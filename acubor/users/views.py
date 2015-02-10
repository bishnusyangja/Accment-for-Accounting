from datetime import date, datetime
import json
import math
import smtplib
from email.mime.text import MIMEText

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import generics
from django.contrib import messages
from django.contrib.auth.models import Group
from mptt.templatetags.mptt_tags import cache_tree_children
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from payroll.models import AttendanceLedger
from users.forms import UserRegistrationForm, CompanyForm
from users.serializers import UserSerializer
from users.models import Company, Role, User, group_required, UserSalesAttachment, UserBankAttachment, \
    UserPurchaseAttachment, UserOtherAttachment, create_default
from ledger.models import Category, Transaction, Account
from dayjournal.models import DayJournal
from django.views.decorators.csrf import csrf_exempt
from payroll.models import Employee
from payroll.views import hr_24


def start_s(request):
    lis = Transaction.objects.filter(account__company=request.user.currently_activated_company).values_list(
        'journal_entry__date', flat=True).order_by('journal_entry__date')[:1]
    if len(lis) > 0:
        return lis[0]
    return None


def start():
    return date(date.today().year - 1, 12, 31)


def end():
    return date.today()


def find_node(mynode, node):
    value = None
    for item in mynode:
        if value is not None:
            break
        if item.name == node:
            value = item
            break

        else:
            if item.is_leaf_node():
                for i in item.accounts.all():
                    if i.name == node:
                        value = i
                        break
            else:
                value = find_node(item.get_children(), node)
    return value


def get_node(request, node):
    # root = cache_tree_children(Category.objects.filter(company=request.user.currently_activated_company))
    try:
        result = Category.objects.get(name=node, company=request.user.currently_activated_company)
    except Category.DoesNotExist:
        result = None
    return result


# get monthly dr for given category up to 12 months exactly
def get_monthly_sum_dr(category):
    mon_data = []
    mon_name = []
    name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year = date.today().year
    month = date.today().month
    if category is not None:
        for i in range(12):
            if month == 0:
                month = 12
                year -= 1
            mon_name.append(name[month - 1])
            mon_data.append(category.get_total_dr(year, month))
            month -= 1
        return mon_name, mon_data
    else:
        return 0, 0


#get monthly cr for given category up to 12 months exactly
def get_monthly_sum_cr(category):
    mon_data = []
    mon_name = []
    name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year = date.today().year
    month = date.today().month
    if category is not None:
        for i in range(12):
            if month == 0:
                month = 12
                year -= 1
            mon_name.append(name[month - 1])
            mon_data.append(category.get_total_cr(year, month))
            month -= 1
        return mon_name, mon_data
    else:
        return 0, 0


#get monthly cr for given category up to this year only
def get_monthly_sum_y(category):
    mon_data = []
    mon_name = []
    name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year = date.today().year
    month = date.today().month
    if category is not None:
        for i in range(12):
            if month == 0:
                break
            mon_name.append(name[month - 1])
            tot = category.get_total_cr(year, month) - category.get_total_dr(year, month)
            mon_data.append(math.fabs(tot))
            month -= 1
        return mon_name, mon_data
    else:
        return 0, 0


def index(request):
    if request.user.is_authenticated():
        cash_account = Account.objects.get(company=request.user.currently_activated_company, name='Cash Account')
        bank_category = Category.objects.get(company=request.user.currently_activated_company, name='Bank Account')
        account_receivable_cat = Category.objects.get(company=request.user.currently_activated_company,
                                                      name='Account Receivables')
        account_payable_cat = Category.objects.get(company=request.user.currently_activated_company,
                                                   name='Account Payables')
        tax_payable_cat = Category.objects.get(company=request.user.currently_activated_company, name='Duties & Taxes')
        latest_dayjournal = DayJournal.objects.filter(company=request.user.currently_activated_company,
                                                      date__lte=end()).order_by('date')
        sales_category = Category.objects.get(company=request.user.currently_activated_company, name='Sales')
        cash_actual = 0.0
        leng = len(latest_dayjournal)
        if leng > 0:
            cash_actual = latest_dayjournal[leng - 1].cash_actual
        else:
            cash_actual = 0.0

        cash_as_per_books = cash_account.get_dr_amount(end()) - cash_account.get_cr_amount(end())
        cash_difference = cash_actual - cash_as_per_books
        sales_total = sales_category.get_duration_cat_tot_cr(start=start(), end=end()) - sales_category.get_duration_cat_tot_dr(start=start(), end=end())

        fuel_sales_total = 0
        if request.user.currently_activated_company.type_of_business in ['Gas Station and Store', 'Gas Station', ]:
            fuel_account = Account.objects.get(company=request.user.currently_activated_company, name="Fuel Sales")
            fuel_sales_total = fuel_account.get_cr_amount(end()) - fuel_account.get_dr_amount(end())
        inside_sales_total = sales_total - fuel_sales_total

        bank_balance_total = bank_category.get_duration_cat_tot_dr(start=start(),
                                                                   end=end()) - bank_category.get_duration_cat_tot_cr(
            start=start(), end=end())
        bank_accounts = Account.objects.filter(company=request.user.currently_activated_company, category=bank_category)
        bank_details = []
        for each in bank_accounts:
            bank_details.append([each.name, each.get_dr_amount(end()) - each.get_cr_amount(end())])

        receivable_total = account_receivable_cat.get_duration_cat_tot_dr(start=start(),
                                                                          end=end()) - account_receivable_cat.get_duration_cat_tot_cr(
            start=start(), end=end())

        payable_total = account_payable_cat.get_duration_cat_tot_cr(start=start(),
                                                                    end=end()) - account_payable_cat.get_duration_cat_tot_dr(
            start=start(), end=end())

        tax_due_upto_date = tax_payable_cat.get_cat_tot_cr(end()) - tax_payable_cat.get_cat_tot_dr(end())
        tax_paid_upto_date = tax_payable_cat.get_cat_tot_dr(end())
        mydata = {}
        mydata['cash_actual'] = cash_actual
        mydata['cash_as_per_books'] = cash_as_per_books
        mydata['cash_difference'] = cash_difference
        mydata['receivable_total'] = receivable_total
        mydata['payable_total'] = payable_total
        mydata['tax_due_upto_date'] = tax_due_upto_date
        mydata['tax_paid_upto_date'] = tax_paid_upto_date
        mydata['bank_balance_total'] = bank_balance_total
        mydata['bank_details'] = bank_details
        mydata['sales_total'] = sales_total
        mydata['fuel_sales_total'] = fuel_sales_total
        mydata['inside_sales_total'] = inside_sales_total
        return render(request, 'dashboard_index.html', mydata)
    # print time.time() - a
    return redirect('/user/login/')


@login_required
def sales_pie_chart(request):
    if request.is_ajax:
        sales = get_node(request, 'Sales')
        if sales is None:
            sales_accounts = None
        else:
            sales_accounts = sales.get_recent_cat_tot(start(), end())
        mydata = {}
        mydata['sales_accounts'] = sales_accounts
        return HttpResponse(json.dumps(mydata), mimetype='application/json')


@login_required
def sales_line_chart(request):
    sales = get_node(request, 'Sales')
    if sales is None:
        mon_name_sales, monthly_sum_sales = None, None
    else:
        mon_name_sales, monthly_sum_sales = get_monthly_sum_cr(sales)
        monthly_sum_sales = map(lambda x: round(x, 2), monthly_sum_sales)
    mydata = {}
    mydata['monthly_sum_sales'] = monthly_sum_sales
    mydata['mon_name_sales'] = mon_name_sales
    return HttpResponse(json.dumps(mydata), mimetype='application/json')


@login_required
def income_expense_chart(request):
    income = get_node(request, 'Income')
    expenses = get_node(request, 'Expenses')
    if income is not None:
        mon_name_income, monthly_sum_income = get_monthly_sum_y(income)
        monthly_sum_income = map(lambda x: round(x, 2), monthly_sum_income)
    else:
        mon_name_income, monthly_sum_income = None, None
    if expenses is not None:
        mon_name_expenses, monthly_sum_expenses = get_monthly_sum_y(expenses)
        monthly_sum_expenses = map(lambda x: round(x, 2), monthly_sum_expenses)
    else:
        mon_name_expenses, monthly_sum_expenses = None, None
    income_amount = income.get_duration_cat_tot_cr(start(), end()) - income.get_duration_cat_tot_dr(start(),
                                                                                                    end()) if income is not None else None
    expenses_amount = expenses.get_duration_cat_tot_dr(start(), end()) - expenses.get_duration_cat_tot_cr(start(),
                                                                                                          end()) if expenses is not None else None

    income_amount = round(income_amount, 2) if income_amount is not None else None
    expenses_amount = round(expenses_amount, 2) if expenses_amount is not None else None
    mydata = {}
    mydata['monthly_sum_income'] = monthly_sum_income
    mydata['mon_name_income'] = mon_name_income
    mydata['monthly_sum_expenses'] = monthly_sum_expenses
    mydata['mon_name_expenses'] = mon_name_expenses
    mydata['income_amount'] = income_amount
    mydata['expenses_amount'] = expenses_amount

    return HttpResponse(json.dumps(mydata), mimetype='application/json')


@login_required
def summaries(request):
    return HttpResponse(json.dumps([]), mimetype='application/json')


def web_login(request, **kwargs):
    if request.user.is_authenticated():

        return redirect('/application/', **kwargs)
    else:
        if request.method == 'POST':
            if request.POST.has_key('remember_me'):
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(6000)
        return login(request, **kwargs)


def home_page(request):
    return render(request, 'homepage.html')


def about_us(request):
    return render(request, 'aboutus.html')


def product_features(request):
    return render(request, 'productfeatures.html')


def logout(request, next_page=None):
    auth_logout(request)
    if next_page:
        return redirect(next_page)
    return redirect('/')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserList(generics.ListCreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer


#def role_management(request):
#roles = Role.objects.get(company=)


def user_setting(request):
    if request.POST:
        request.user.full_name = request.POST['full_name']
        request.user.email = request.POST['email']
        request.user.save()
    return render(request, 'user_setting.html')


def set_company(request, id):
    company = Company.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    user.currently_activated_company = company
    user.save()
    return redirect('/application/')


@group_required('Owner', 'SuperOwner')
def roles(request):
    if request.POST:
        try:
            user = User.objects.get(username=request.POST['user'])
            group = Group.objects.get(name=request.POST['group'])
            try:
                Role.objects.get(user=user, company=request.user.currently_activated_company, group=group)
                messages.error(request,
                               'User ' + user.username + ' (' + user.email + ') is already the ' + request.POST[
                                   'group'] + '.')
            except Role.DoesNotExist:
                existing_roles = Role.objects.filter(user=user, company=request.user.currently_activated_company)
                for existing_role in existing_roles:
                    existing_role.delete()
                role = Role(user=user, company=request.user.currently_activated_company, group=group)
                role.save()
                if str(group) == 'Employee':
                    acc = Account()
                    try:
                        cat = Category.objects.get(name='Employee', company=request.user.currently_activated_company)
                    except Category.DoesNotExist:
                        cat = Category.objects.create(name='Employee', company=request.user.currently_activated_company)
                    acc.category = cat
                    acc.name = user.username
                    acc.company = request.user.currently_activated_company
                    acc.save()

                    emp = Employee()
                    emp.name = user.username
                    emp.user = user
                    emp.company = request.user.currently_activated_company
                    emp.account = acc
                    emp.save()

                messages.success(request,
                                 'User ' + user.username + ' (' + user.email + ') added as ' + request.POST[
                                     'group'] + '.')
        except User.DoesNotExist:
            messages.error(request, 'No users found with the username ' + request.POST['user'])
    objs = Role.objects.filter(company=request.user.currently_activated_company)
    return render(request, 'roles.html', {'roles': objs})


def delete_role(request, id):
    obj = Role.objects.get(company=request.user.currently_activated_company, id=id)
    if not obj.group.name == 'SuperOwner':
        obj.delete()
    return redirect(reverse('roles'))


def user_attachments(request):
    sales_attachments = UserSalesAttachment.objects.filter(company=request.user.currently_activated_company)
    purchase_attachments = UserPurchaseAttachment.objects.all()
    bank_attachments = UserBankAttachment.objects.all()
    other_attachments = UserOtherAttachment.objects.all()
    data = {}
    data['sales_attachments'] = sales_attachments
    data['purchase_attachments'] = purchase_attachments
    data['bank_attachments'] = bank_attachments
    data['other_attachments'] = other_attachments
    return render(request, 'users_attachments.html', data)


import os
from settings import MEDIA_ROOT


@login_required
def delete_user_attachments(request):
    if request.POST['type'] == 'sales':
        obj = get_object_or_404(UserSalesAttachment, company=request.user.currently_activated_company,
                                id=request.POST['id'])
        path = os.path.join(MEDIA_ROOT, str(obj.attachment))
        os.remove(path)
        obj.delete()
    elif request.POST['type'] == 'purchase':
        obj = get_object_or_404(UserPurchaseAttachment, company=request.user.currently_activated_company,
                                id=request.POST['id'])
        path = os.path.join(MEDIA_ROOT, str(obj.attachment))
        os.remove(path)
        obj.delete()
    elif request.POST['type'] == 'other':
        obj = get_object_or_404(UserOtherAttachment, company=request.user.currently_activated_company,
                                id=request.POST['id'])
        path = os.path.join(MEDIA_ROOT, str(obj.attachment))
        os.remove(path)
        obj.delete()
    elif request.POST['type'] == 'bank':
        obj = get_object_or_404(UserBankAttachment, company=request.user.currently_activated_company,
                                id=request.POST['id'])
        path = os.path.join(MEDIA_ROOT, str(obj.attachment))
        os.remove(path)
        obj.delete()
    return HttpResponse(json.dumps({'success': True}), mimetype="application/json")


@login_required
def save_user_attachments(request):
    if request.POST['type'] == 'sales':
        model = UserSalesAttachment
    elif request.POST['type'] == 'purchase':
        model = UserPurchaseAttachment
    elif request.POST['type'] == 'other':
        model = UserOtherAttachment
    elif request.POST['type'] == 'bank':
        model = UserBankAttachment
    captions = request.POST.getlist('captions')
    attachments = request.FILES.getlist('attachments')

    lst = []
    for i, attachment in enumerate(attachments):
        attached = model(attachment=attachment, description=captions[i],
                         company=request.user.currently_activated_company)
        attached.uploaded_date = date.today()
        attached.uploaded_time = datetime.now()
        attached.save()
        lst.append(
            {'name': attachment.name, 'caption': captions[i], 'id': attached.id, 'link': attached.attachment.url})
    return HttpResponse(json.dumps(lst), mimetype="application/json")


@login_required
def attachment_process(request):
    dct = {}
    obj_id = request.POST.get('id')
    obj_type = request.POST.get('type')
    process = request.POST.get('process')
    print obj_type
    if obj_type == 'sales':
        model = UserSalesAttachment
    elif obj_type == 'purchase':
        model = UserPurchaseAttachment
    elif obj_type == 'bank':
        model = UserBankAttachment
    else:
        model = UserOtherAttachment
    try:
        obj = model.objects.get(id=obj_id, company=request.user.currently_activated_company)
        if process == 'process':
            obj.is_processed = change_state(obj.is_processed)
            if obj.is_processed:
                obj.processed_date = date.today()
            else:
                obj.processed_date = None
            obj.save()
        elif process == 'approve':
            obj.is_approved = change_state(obj.is_approved)
            obj.save()
        elif process == 'delete':
            delete_attachment(obj)
        else:
            dct['error_message'] = ('Requested process not found!')
    except model.DoesNotExist:
        dct['error_message'] = ('Requested object not found!')

    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def list_user_attachments(request):
    sales_attachments = UserSalesAttachment.objects.filter(company=request.user.currently_activated_company).order_by('-uploaded_date', '-uploaded_time')
    purchase_attachments = UserPurchaseAttachment.objects.filter(company=request.user.currently_activated_company).order_by('-uploaded_date', '-uploaded_time')
    bank_attachments = UserBankAttachment.objects.filter(company=request.user.currently_activated_company).order_by('-uploaded_date', '-uploaded_time')
    other_attachments = UserOtherAttachment.objects.filter(company=request.user.currently_activated_company).order_by('-uploaded_date', '-uploaded_time')
    return render(request, 'list_user_attachments.html', {
        'sales_attachments': sales_attachments,
        'purchase_attachments': purchase_attachments,
        'bank_attachments': bank_attachments,
        'other_attachments': other_attachments
    })


############ NEW USER REQUEST  ##### URL IS /user/request-new-user/
from django.contrib.auth.hashers import make_password
from settings import EMAIL_HOST
from django.core.validators import validate_email

from django.forms import EmailField
from django.core.exceptions import ValidationError


def isemailvalid(email):
    try:
        EmailField().clean(email)
        return True
    except ValidationError:
        return False


@login_required
def request_new_user(request):
    from collections import Counter
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        group = request.POST.get('group')
        full_name = request.POST.get('fullname', '')
        full_name = full_name.strip()
        name_dict = Counter(full_name)
        print request.user, request.user.currently_activated_company
        obj_user = User.objects.filter(username=username)
        obj_name = User.objects.filter(full_name=full_name, currently_activated_company=request.user.currently_activated_company)
        if name_dict[' '] > 1:
            error = 'Multiple spaces are not allowed. Use only one space for full name.'
            return render(request, 'request_new_user.html', {'error': error})

        if len(obj_name) > 0:
            error = 'User with full name ' + full_name + 'already exists.'
            return render(request, 'request_new_user.html', {'error': error})

        if len(obj_user) > 0:
            error = "Username " + username + " already Exists!"
            return render(request, 'request_new_user.html', {'error': error})
        else:
            password = User.objects.make_random_password(length=10)
            passwd = make_password(password)
            if isemailvalid(email):
                obj = User.objects.create(username=username, email=email, password=passwd, is_active=True,
                                          full_name=full_name)
                message = "Please use %s as your Username and %s as Password to login in Accment.com . You can change password later." % (
                    username, password)

                obj.email_user(subject=" You have been registered at Accment", message=message, from_email=EMAIL_HOST)
                grp = Group.objects.get(name=group)
                Role.objects.create(user=obj, group=grp, company=request.user.currently_activated_company)
                if grp.name == "Employee":
                    acc = Account()
                    try:
                        cat = Category.objects.get(name='Employee', company=request.user.currently_activated_company)
                    except Category.DoesNotExist:
                        cat = Category.objects.create(name='Employee', company=request.user.currently_activated_company)
                    acc.category = cat
                    acc.name = full_name
                    acc.company = request.user.currently_activated_company
                    if request.user.currently_activated_company.current_financial_year_started_on:
                        acc.opening_as_on_date = request.user.currently_activated_company.current_financial_year_started_on
                    acc.save()

                    emp = Employee()
                    emp.name = full_name
                    emp.user = obj
                    emp.company = request.user.currently_activated_company
                    emp.account = acc
                    emp.save()
            else:
                error = "Invalid Email Address"
                return render(request, 'request_new_user.html', {'error': error})

    return render(request, 'request_new_user.html')


@login_required
def save_time(request):
    dct = {}
    error = None
    if request.is_ajax():
        attr = request.POST.get('id')
        day = request.POST.get('day')
        time = request.POST.get('time')
        try:
            employee = Employee.objects.get(user=request.user.id, company=request.user.currently_activated_company)
        except Employee.DoesNotExist:
            employee = None
        # except Employee.MultipleObjectsReturned:
        #     employee = None
        if employee is not None:
            attendance, created = AttendanceLedger.objects.get_or_create(employee=employee, date=day)
        else:
            attendance = None
        if attendance is not None:
            if attr == 'time-in1':
                if not attendance.in_time1:
                    attendance.in_time1 = hr_24(time)
                    attendance.save()
                else:
                    error = 'This much for today.'
            elif attr == 'time-out1':
                if not attendance.out_time1:
                    attendance.out_time1 = hr_24(time)
                    attendance.save()
                else:
                    error = 'This much for today.'
            elif attr == 'time-in2':
                if not attendance.in_time2:
                    attendance.in_time2 = hr_24(time)
                    attendance.save()
                else:
                    error = 'This much for today.'
            elif attr == 'time-out2':
                if not attendance.out_time2:
                    attendance.out_time2 = hr_24(time)
                    attendance.save()
                else:
                    error = 'This much for today.'
            else:
                error = 'This is not correct option.'
        else:
            error = "You have no role employee."
    if error is not None:
        dct['error'] = error
        # print dct['error']
    return HttpResponse(json.dumps(dct), mimetype='application/json')


@login_required
def company_setup(request, id=None):
    if id:
        obj = get_object_or_404(Company, id=id)
    else:
        obj = Company()
    if request.POST:
        form = CompanyForm(data=request.POST)
        if form.is_valid():
            obj.name = form.cleaned_data['name']
            obj.address_line_1 = form.cleaned_data['street_address_1']
            obj.address_line_2 = form.cleaned_data['street_address_2']
            obj.city = form.cleaned_data['city']
            obj.state = form.cleaned_data['state']
            obj.zip_code = form.cleaned_data['zip_code']
            obj.type_of_business = form.cleaned_data['type_of_business']
            obj.save()
            create_default(obj, obj.type_of_business, dict(form.data))
            grp = Group.objects.get(name='SuperOwner')
            Role.objects.create(user=request.user, group=grp, company=obj)
            return redirect('/user/set-company/' + str(obj.id) + '/')
    else:
        form = CompanyForm()

    return render(request, 'company_setup.html', {'form': form})


from users.models import TrackUserInfo


@login_required
def get_ip_infos(request):
    tracked_datas = TrackUserInfo.objects.all().order_by('ipaddress')
    return render(request, "ip_infos.html", {'tracked_data': tracked_datas})


def change_state(value):
    if value:
        return False
    else:
        return True


def delete_attachment(obj):
    path = os.path.join(MEDIA_ROOT, str(obj.attachment))
    os.remove(path)
    obj.delete()


@login_required
def subscription_status(request):
    return render(request, 'user_subscriptions.html')
