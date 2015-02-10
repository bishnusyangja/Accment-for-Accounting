from datetime import date, datetime
import json

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from payroll.models import Employee, GroupPayroll, GroupPayrollRow, \
    IndividualPayroll, Inclusion, Deduction, AttendanceLedger, AttendanceParameter
from payroll.serializers import EmployeeSerializer, GroupPayrollSerializer, IndividualPayrollSerializer, AttendanceLedgerSerializer, AttendanceParameterSerializer
from lib import save_model, invalid, empty_to_zero
from ledger.models import delete_rows, set_transactions, Account, Category, JournalEntry
from payroll.forms import EmployeeForm, AttendanceParameterForm
from users.models import group_required


@login_required
def employee_form(request, id=None):
    if id:
        obj = get_object_or_404(Employee, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
    else:
        obj = Employee(company=request.user.currently_activated_company)
        scenario = 'Create'
    message = None
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'

    if request.POST:
        form = EmployeeForm(data=request.POST, instance=obj, company=request.user.currently_activated_company)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.company = request.user.currently_activated_company
            if not obj.user:
                obj.user = None
            name_list = Employee.objects.filter(name=obj.name.strip(), company=request.user.currently_activated_company)
            ledger_list = Account.objects.filter(name=obj.name.strip(), company=request.user.currently_activated_company,
                                                 category__name='Employee')
            if scenario == "Create":
                if name_list or ledger_list:
                    msg = 'Duplicate name is not allowed.'
                    return render(request, 'employee_form.html', {
                            'scenario': scenario,
                            'form': form,
                            'msg': msg,
                            'base_template': base_template,
                        })
            cat = Category.objects.get(name='Employee', company=request.user.currently_activated_company)
            acc = Account(name=obj.name, company=request.user.currently_activated_company, category=cat, opening_as_on_date=request.user.currently_activated_company.settings.current_financial_year_started_on)
            acc.save()
            obj.account = acc
            obj.save()


            message = "Saved!"
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': EmployeeSerializer(obj).data})
            return render(request, 'employee_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
        'message': message,

    })
    else:
        form = EmployeeForm(instance=obj, company=request.user.currently_activated_company)

    return render(request, 'employee_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
        'message': message
    })


@login_required
def list_employees(request):
    objs = Employee.objects.filter(company=request.user.currently_activated_company)
    return render(request, 'list_employees.html', {'objects': objs})


@login_required
def employees_as_json(request):
    objs = Employee.objects.filter(company=request.user.currently_activated_company).order_by('name')
    objs_data = EmployeeSerializer(objs).data
    return HttpResponse(json.dumps(objs_data), mimetype="application/json")


@login_required
def attendance_parameter_as_json(request):
    objs = AttendanceParameter.objects.filter(company=request.user.currently_activated_company)
    objs_data = AttendanceParameterSerializer(objs).data
    return HttpResponse(json.dumps(objs_data), mimetype="application/json")


@login_required
def delete_employee(request, id):
    obj = get_object_or_404(Employee, id=id, company=request.user.currently_activated_company)
    obj.delete()
    return redirect(reverse_lazy('list_employees'))


@login_required
def group_payroll_voucher(request, id=None):
    factor = AttendanceParameter.objects.filter(company=request.user.currently_activated_company)
    disabled = False
    if not factor:
        disabled = True
    approved = 0
    if id:
        voucher = get_object_or_404(GroupPayroll, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
        voucher.date = voucher.date.strftime('%m/%d/%Y')
        voucher.from_date = voucher.from_date.strftime('%m/%d/%Y')
        voucher.to_date = voucher.to_date.strftime('%m/%d/%Y')
    else:
        voucher = GroupPayroll(date=date.today().strftime('%m/%d/%Y'))
        scenario = 'Create'
        voucher.voucher_no = voucher.get_wt_voucher_no(request)
    data = GroupPayrollSerializer(voucher).data

    if data['status'] == 'Approved':
        approved = 1

    return render(request, 'group_payroll_voucher.html', {'scenario': scenario, 'data': data, 'approved': approved,
                                                          'disabled': disabled})


@login_required
def save_group_payroll_voucher(request):
    params = json.loads(request.body)
    dct = {'rows': {}}

    vch_no = params.get('voucher_no')
    try:
        vch_no = int(vch_no)
    except ValueError:
        dct['error_message'] = 'Only numbers are allowed in voucher no.'
        return HttpResponse(json.dumps(dct), mimetype='application/json')

    voucher_values = {'date': params.get('date'), 'voucher_no': params.get('voucher_no'), 'company': request.user.currently_activated_company,
                      'from_date': params.get('from_date'), 'to_date': params.get('to_date')}
    if params.get('id'):
        voucher = GroupPayroll.objects.get(id=params.get('id'))
    else:
        voucher = GroupPayroll()
    res1 = voucher_values['date'].encode('utf-8').split("/")
    voucher_values['date'] = res1[2] + '-' + res1[0] + '-' + res1[1]

    res = voucher_values['from_date'].encode('utf-8').split("/")
    voucher_values['from_date'] = res[2] + '-' + res[0] + '-' + res[1]

    res = voucher_values['to_date'].encode('utf-8').split("/")
    voucher_values['to_date'] = res[2] + '-' + res[0] + '-' + res[1]

    voucher = save_model(voucher, voucher_values)
    dct['id'] = voucher.id
    model = GroupPayrollRow
    for index, row in enumerate(params.get('table_vm').get('rows')):
        if invalid(row, ['employee', 'pay_head']):
            continue
        rate_day = empty_to_zero(row.get('rate_day'))
        rate_hour = empty_to_zero(row.get('rate_hour'))
        # rate_ot_hour = empty_to_zero(row.get('rate_ot_hour'))
        values = {'employee_id': row.get('employee'), 'rate_day': rate_day,
                  'rate_hour': rate_hour, 'present_days': row.get('present_days'),
                  'present_hours': row.get('present_hours'),
                  'payroll_tax': row.get('payroll_tax'), 'pay_head_id': row.get('pay_head'),
                  'group_payroll': voucher}

        if not values['payroll_tax']:
            values['payroll_tax'] = 0
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('table_vm').get('deleted_rows'), model)
    voucher.status = 'Unapproved'
    voucher.save()

    ledger = AttendanceLedger.objects.filter(date__lte=voucher.to_date, date__gte=voucher.from_date,
                                             employee=submodel.employee)
    for item in ledger:
        item.content_type = ContentType.objects.get(model='grouppayroll')
        item.object_id = voucher.id
        item.save()

    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('create_group_payroll_voucher'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('SuperOwner', 'Owner', 'Supervisor')
def approve_group_payroll_voucher(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        voucher = GroupPayroll.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    voucher.backend_approve(request)
    dct['redirect_to'] = '/payroll/group-voucher/' + str(params.get('id')) + '/'
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def delete_group_payroll_voucher(request, id):
    obj = get_object_or_404(GroupPayroll, id=id, company=request.user.currently_activated_company)
    obj.delete()
    return redirect(reverse_lazy('create_group_payroll_voucher'))


@login_required
def individual_payroll_voucher(request, id=None):
    factor = AttendanceParameter.objects.filter(company=request.user.currently_activated_company)
    disabled = False
    if not factor:
        disabled = True
    approved = 0
    if id:
        voucher = get_object_or_404(IndividualPayroll, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
        voucher.date = voucher.date.strftime('%m/%d/%Y')
        voucher.from_date = voucher.from_date.strftime('%m/%d/%Y')
        voucher.to_date = voucher.to_date.strftime('%m/%d/%Y')
    else:
        voucher = IndividualPayroll(date=date.today().strftime("%m/%d/%Y"))
        scenario = 'Create'
        voucher.voucher_no = voucher.get_wt_voucher_no(request)
    data = IndividualPayrollSerializer(voucher).data
    if data['status'] == 'Approved':
        approved = 1
    employee_deductions = Category.objects.get(name='Employee Deductions', company=request.user.currently_activated_company)
    pay_head = Category.objects.get(name='Pay Head', company=request.user.currently_activated_company)
    return render(request, 'individual_payroll_voucher.html',
                  {'scenario': scenario, 'data': data, 'approved': approved, 'employee_deductions': employee_deductions,
                   'pay_head': pay_head, 'disabled': disabled})


@login_required
def save_individual_payroll_voucher(request):
    params = json.loads(request.body)
    dct = {'rows1': {}, 'rows2': {}}
    vch_no = params.get('voucher_no')
    try:
        vch_no = int(vch_no)
    except ValueError:
        dct['error_message'] = 'Only numbers are allowed in voucher no.'
        return HttpResponse(json.dumps(dct), mimetype='application/json')

    voucher_values = {'date': params.get('date'), 'voucher_no': params.get('voucher_no'),
                      'days_worked': params.get('days_worked'),
                      'hours_worked': params.get('hours_worked'), 'from_date': params.get('from_date'),
                      'to_date': params.get('to_date'),
                      'day_rate': params.get('day_rate'), 'hour_rate': params.get('hour_rate'),
                      'employee_id': params.get('employee'), 'company': request.user.currently_activated_company, }
    res = voucher_values['date'].encode('utf-8').split("/")
    voucher_values['date'] = res[2] + '-' + res[0] + '-' + res[1]

    res = voucher_values['from_date'].encode('utf-8').split("/")
    voucher_values['from_date'] = res[2] + '-' + res[0] + '-' + res[1]

    res = voucher_values['to_date'].encode('utf-8').split("/")
    voucher_values['to_date'] = res[2] + '-' + res[0] + '-' + res[1]

    if params.get('id'):
        voucher = IndividualPayroll.objects.get(id=params.get('id'))
    else:
        voucher = IndividualPayroll()
    voucher = save_model(voucher, voucher_values)
    dct['id'] = voucher.id
    model = Inclusion
    for index, row in enumerate(params.get('inclusions').get('rows')):
        if invalid(row, ['account', 'amount']):
            continue
        values = {'particular_id': row.get('account'), 'amount': row.get('amount'), 'individual_payroll': voucher}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows1'][index] = submodel.id
    delete_rows(params.get('inclusions').get('deleted_rows'), model)
    model = Deduction
    for index, row in enumerate(params.get('deductions').get('rows')):
        if invalid(row, ['account', 'amount']):
            continue
        values = {'particular_id': row.get('account'), 'amount': row.get('amount'), 'individual_payroll': voucher}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows2'][index] = submodel.id
    delete_rows(params.get('deductions').get('deleted_rows'), model)
    voucher.status = 'Unapproved'
    voucher.save()

    ledger = AttendanceLedger.objects.filter(date__lte=voucher.to_date, date__gte=voucher.from_date,
                                             employee=voucher.employee)
    for item in ledger:
        item.content_type = ContentType.objects.get(model='individualpayroll')
        item.object_id = voucher.id
        item.save()

    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('create_individual_payroll_voucher'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('SuperOwner', 'Owner', 'Supervisor')
def approve_individual_payroll_voucher(request):
    params = json.loads(request.body)
    dct = {}

    if params.get('id'):
        voucher = IndividualPayroll.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    voucher.backend_approve(request)
    dct['redirect_to'] = '/payroll/individual-voucher/' + str(params.get('id')) + '/'
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def delete_individual_payroll_voucher(request, id):
    obj = get_object_or_404(IndividualPayroll, id=id, company=request.user.currently_activated_company)
    obj.delete()
    return redirect(reverse_lazy('create_individual_payroll_voucher'))


@login_required
def payroll_register(request):
    group_items = GroupPayrollRow.objects.filter(group_payroll__company=request.user.currently_activated_company).order_by(
        '-group_payroll__date', 'group_payroll__id')
    individual_items = IndividualPayroll.objects.filter(company=request.user.currently_activated_company).order_by('-date', 'id')
    myinclusion = []
    mydeduction = []
    for item in individual_items:
        inclus = Inclusion.objects.filter(individual_payroll__id=item.id, individual_payroll__company=request.user.currently_activated_company)
        deduc = Deduction.objects.filter(individual_payroll__id=item.id, individual_payroll__company=request.user.currently_activated_company)
        myinclusion.append(inclus)
        mydeduction.append(deduc)
    mylist = [myinclusion, mydeduction]
    return render(request, 'list_payroll.html', {'group_items': group_items,
                                                 'individual_items': individual_items,
                                                 'mylist': mylist
    })


@group_required('SuperOwner', 'Owner', 'Supervisor')
def unapprove_group_payroll_voucher(request, id):
    dct = {}
    obj = GroupPayroll.objects.get(company=request.user.currently_activated_company, id=id)
    obj.backend_unapprove()
    dct['redirect_to'] = '/payroll/group-voucher/' + str(id) + '/'
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('SuperOwner', 'Owner', 'Supervisor')
def unapprove_individual_payroll_voucher(request, id):
    dct = {}
    obj = IndividualPayroll.objects.get(company=request.user.currently_activated_company, id=id)
    obj.backend_unapprove()

    dct['redirect_to'] = '/payroll/individual-voucher/' + str(id) + '/'
    return HttpResponse(json.dumps(dct), mimetype="application/json")


# to get the index of the month: 0 for january
def get_month(month):
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
              'november', 'december']
    try:
        index = months.index(month)
    except ValueError:
        index = -1
    return index


@login_required
def employee_detail(request):
    employee = int(request.POST.get('employee'))
    start = manage_start_date(request, employee)
    end = formatting_date(request.POST.get('end', ''))
    if end is '':
        end = date.today()
    obj = Employee.objects.get(id=employee)
    worked_days = obj.get_unpaid_worked_days(start, end)
    worked_hours = obj.get_unpaid_worked_hours(start, end)

    s_date = str(start).split('-')
    start = s_date[1] + '/' + s_date[2] + '/' + s_date[0]

    data = {'worked_days': worked_days, 'worked_hours': worked_hours, 'start': start}
    return HttpResponse(json.dumps(data), mimetype='application/json')


# Them modified payroll contents are all below this comment
def attendance_ledger(request):
    if request.is_ajax():
        employee = request.POST.get('employee')
        try:
            month = request.POST.get('month')
        except ValueError:
            month = 'january'
        if employee and month:
            try:
                ledger = AttendanceLedger.objects.filter(employee=employee, date__month=get_month(month) + 1,
                                                         ).order_by('date')
            except AttendanceLedger.DoesNotExist:
                ledger = AttendanceLedger()

            data = AttendanceLedgerSerializer(ledger).data

            return HttpResponse(json.dumps(data), mimetype="application/json")
    return render(request, 'attendance_ledger.html')


def save_attendance_ledger(request):
    dct = {}
    params = json.loads(request.body)
    attendance_type = params.get('attendance_type')
    if attendance_type == 'day_attendance':
        for row in params.get('day_attendance'):
            if row.get('attendance_status'):
                if row.get('paid') == 'Paid':
                    paid = True
                else:
                    paid = False

                values = {'employee': params.get('employee'), 'attendance_type': params.get('attendance_type'),
                          'date': row.get('date'), 'attendance_status': row.get('attendance_status'), 'paid': paid}
                d = values['date'].encode('utf-8').split('/')
                values['date'] = d[2] + '-' + d[0] + '-' + d[1]
                employee = Employee.objects.get(id=values['employee'])
                values['employee'] = employee
                try:
                    attendance = AttendanceLedger.objects.get(employee=employee, date=values['date'])
                except  AttendanceLedger.DoesNotExist:
                    attendance = AttendanceLedger()
                save_model(attendance, values)

    if attendance_type == 'hour_attendance':
        for row in params.get('hour_attendance'):
            if (row.get('in_time1') and row.get('out_time1')) or (row.get('in_time2') and row.get('out_time2')):
                values = {'employee': params.get('employee'), 'attendance_type': params.get('attendance_type'),
                          'date': row.get('date')}
                if row.get('in_time1'):
                    values['in_time1'] = hr_24(row.get('in_time1'))
                    values['out_time1'] = hr_24(row.get('out_time1'))
                if row.get('in_time2'):
                    values['in_time2'] = hr_24(row.get('in_time2'))
                    values['out_time2'] = hr_24(row.get('out_time2'))

                d = values['date'].encode('utf-8').split('/')
                values['date'] = d[2] + '-' + d[0] + '-' + d[1]
                employee = Employee.objects.get(id=values['employee'])
                values['employee'] = employee
                try:
                    attendance = AttendanceLedger.objects.get(employee=employee, date=values['date'])
                except AttendanceLedger.DoesNotExist:
                    attendance = AttendanceLedger()
                save_model(attendance, values)

    return HttpResponse(json.dumps(dct), mimetype='application/json')


@login_required
def delete_hour_attendance(request):
    day = request.GET.get('date')
    employee = request.GET.get('employee')
    emp = Employee.objects.get(id=employee)
    res = day.split('/')
    day = res[2] + '-' + res[0] + '-' + res[1]
    try:
        obj = AttendanceLedger.objects.get(date=day, employee=emp)
        obj.in_time1 = None
        obj.in_time2 = None
        obj.out_time1 = None
        obj.out_time2 = None
        obj.save()
    except AttendanceLedger.DoesNotExist:
        print 'Requested object is not found'
    return HttpResponse('success')


@login_required
def delete_day_attendance(request):
    day = request.GET.get('date')
    employee = request.GET.get('employee')
    emp = Employee.objects.get(id=employee)
    res = day.split('/')
    day = res[2] + '-' + res[0] + '-' + res[1]
    try:
        obj = AttendanceLedger.objects.get(date=day, employee=emp)
        print obj
        obj.attendance_status = ''
        obj.save()
    except AttendanceLedger.DoesNotExist:
        print 'Requested object is not found'
    return HttpResponse('success')


def hr_24(value):
    if value:

        my_string = str(value)
        my_string = my_string.upper()

        if my_string.split(':')[0] == '12':
            if my_string.find('A') >= 0:
                my_string = my_string.replace('A', 'P')
            else:
                my_string = my_string.replace('P', 'A')
        if my_string.split(' ')[1] == 'PM':
            hr = int(my_string.split(':')[0])
            hr += 12
            if hr >= 24:
                hr -= 24
            hrm = my_string.split(':')
            my_string = str(hr) + ':' + hrm[1]
            my_string = my_string.replace(' PM', '')
        else:
            my_string = my_string.replace(' AM', '')
        return my_string
    else:
        return value


def formatting_date(d):
    # d = d.encode('utf-8').split('/')
    # return d[2] + '-' + d[0] + '-'+ d[1]
    d = str(d)
    if d.find('/') >= 0:
        d = d.encode('utf-8').split('/')
        return d[2] + '-' + d[0] + '-' + d[1]
    else:
        return d


def manage_start_date(request, employee):
    start = request.POST.get('start', '')
    if start is '':
        start = AttendanceLedger.objects.filter(employee=employee, paid=False).order_by('date')
        if len(start) > 0:
            start = start[0].date
        else:
            start = date.today()
    else:
        start = formatting_date(start)
    return start


@login_required
def attendance_parameter(request, next=None):
    obj = AttendanceParameter.objects.filter(company=request.user.currently_activated_company)
    if obj:
        factor = obj[0]
        scenario = 'Update'
    else:
        factor = AttendanceParameter()
        scenario = 'Create'
    if request.POST:
        form = AttendanceParameterForm(data=request.POST, instance=factor)
        if form.is_valid():
            new_obj = form.save()
            new_obj.company = request.user.currently_activated_company
            new_obj.save()
            redirect_to = '/payroll/'+next+'/'
            return redirect(redirect_to)
    else:
        form = AttendanceParameterForm(instance=factor)
        return render(request, 'attendance_parameter.html', {'form': form, 'scenario': scenario})
