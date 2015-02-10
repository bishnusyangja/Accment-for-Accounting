import json
from datetime import date

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from forms import CashReceiptForm, CashPaymentForm, InvoiceForm, PurchaseVoucherForm
from filters import InvoiceFilter
from users.models import group_required, create_license_required, view_license_required
from models import Invoice, PurchaseVoucher, JournalVoucher, InvoiceParticular, PurchaseParticular,\
    JournalVoucherRow, CashReceipt, CashReceiptRow, CashPayment, CashPaymentRow, FixedAsset, FixedAssetRow, AdditionalDetail
from serializers import JournalVoucherSerializer, CashReceiptSerializer, CashPaymentSerializer, \
    FixedAssetSerializer, InvoiceSerializer, InvoiceParticularSerializer, PurchaseVoucherSerializer
from lib import invalid, save_model, all_empty_in_dict
from ledger.models import delete_rows, Account, set_transactions, Party, Category, JournalEntry, Transaction, \
    _transaction_delete
from templatetags.filters import handler
import watson
from bank.models import BankPayment, BankDeposit
from dayjournal.models import DayJournal
from payroll.models import GroupPayroll, IndividualPayroll

from django.db import transaction


@login_required
def all_invoices(request):
    items = Invoice.objects.filter(company=request.user.currently_activated_company)
    # filtered_items = InvoiceFilter(request.GET, queryset=items, company=request.user.currently_activated_company)
    if request.method == "POST":
        search_text = request.POST.get('search-text')
        result = watson.search(search_text,models=(Invoice.objects.filter(company=request.user.currently_activated_company), \
                                                   InvoiceParticular.objects.filter(invoice__company=request.user.currently_activated_company)))
        result_obj = [res.object for res in result]
        res = []
        for item in result_obj:
            if type(item) == InvoiceParticular:
                res.append(item.invoice)
            if type(item) == Invoice:
                res.append(item)
        res = list(set(res))
        return render(request, 'list_invoice.html', {'objects': res})
    return render(request, 'list_invoice.html', {'objects': items})


@login_required
def invoice(request, id=None):
    from core.models import VoucherSetting
    from core.models import CompanySetting
    approved = 0

    try:
        voucher_setting = VoucherSetting.objects.get(company=request.user.currently_activated_company)
        company_setting = CompanySetting.objects.get(company=request.user.currently_activated_company)
    except CompanySetting.DoesNotExist:
        #TODO Add a flash message
        return redirect('/settings/company')
    if id:
        invoice_obj = get_object_or_404(Invoice, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
        if invoice_obj.status == 'Approved':
            approved = 1
    else:
        invoice_obj = Invoice(company=request.user.currently_activated_company)
        scenario = 'Create'
        invoice_obj.due_date = date.today()
        invoice_obj.date = date.today()
    form = InvoiceForm(data=request.POST, instance=invoice_obj, company=request.user.currently_activated_company)
    invoice_data = InvoiceSerializer(invoice_obj).data
    if invoice_data['date']:
        invoice_data['date'] = invoice_data['date'].strftime("%m/%d/%Y")
    if invoice_data['due_date']:
        invoice_data['due_date'] = invoice_data['due_date'].strftime("%m/%d/%Y")
    invoice_data['read_only'] = {
        'invoice_prefix': voucher_setting.invoice_prefix,
        'invoice_suffix': voucher_setting.invoice_suffix,
    }
    return render(request, 'invoice.html', {'form': form, 'data': invoice_data, 'scenario': scenario, 'approved': approved})


@login_required
def save_invoice(request):
    params = json.loads(request.body)
    dct = {'rows': {}}

    vch_no = params.get('voucher_no')
    try:
        vch_no = int(vch_no)
    except ValueError:
        dct['error_message'] = 'Only numbers are allowed in voucher no.'
        return HttpResponse(json.dumps(dct), mimetype='application/json')

    if params.get('id'):
        invoice_obj = Invoice.objects.get(id=params.get('id'), company=request.user.currently_activated_company)
    else:
        invoice_obj = Invoice(company=request.user.currently_activated_company)
        # if not created:
    try:
        existing = Invoice.objects.get(voucher_no=params.get('voucher_no'), company=request.user.currently_activated_company)
        if invoice_obj.id is not existing.id:
            return HttpResponse(json.dumps({'error_message': 'Invoice No. already exists'}),
                                mimetype="application/json")
    except Invoice.DoesNotExist:
        pass
    invoice_values = {'party_id': params.get('party'), 'voucher_no': params.get('voucher_no'),
                      'description': params.get('description'),
                      'reference': params.get('reference'),
                      'date': date(int(params.get('date').split('/')[2]), int(params.get('date').split('/')[0]),
                                   int(params.get('date').split('/')[1])),
                      'due_date': date(int(params.get('due_date').split('/')[2]), int(params.get('due_date').split('/')[0]),
                                   int(params.get('due_date').split('/')[1])),
                      'tax': params.get('tax'),
                      'currency_id': params.get('currency'), 'company': request.user.currently_activated_company, 'status': 'Unapproved',
                      'pending_amount': params.get('total_amount'), 'total_amount': params.get('total_amount')}
    if invoice_values['total_amount'] == '':
        invoice_values['total_amount'] = 0
    if invoice_values['pending_amount'] == '':
        invoice_values['pending_amount'] = 0
    invoice_obj = save_model(invoice_obj, invoice_values)
    dct['id'] = invoice_obj.id
    model = InvoiceParticular
    for index, row in enumerate(params['particulars']['rows']):
        if row.get('discount') == '':
            row['discount'] = 0
        values = {'sn': index + 1, 'account_id': row.get('account'), 'description': row.get('description'),
                  'unit_price': row.get('unit_price'), 'quantity': row.get('quantity'), 'discount': row.get('discount'),
                  'tax_scheme_id': row.get('tax_scheme'), 'invoice': invoice_obj}
        # print row.get('id')
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('particulars').get('deleted_rows'), model)
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('new_invoice'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Owner', 'SuperOwner', 'Supervisor')
def approve_invoice(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        voucher = Invoice.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    status = voucher.backend_approve()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Owner', 'SuperOwner', 'Supervisor')
def unapprove_invoice(request, id):
    dct = {}
    try:
        invoice = Invoice.objects.get(id=id, company=request.user.currently_activated_company)
    except:
        dct['error_message'] = 'Voucher can not be approved.'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    status = invoice.backend_unapprove()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def cancel_invoice(request):
    r = save_invoice(request)
    dct = json.loads(r.content)
    obj = Invoice.objects.get(id=dct.get('id'))
    obj.status = 'Cancelled'
    obj.save()
    return r


@login_required
def delete_invoice(request, id):
    obj = Invoice.objects.get(id=id, company=request.user.currently_activated_company)
    obj.delete()
    return redirect(reverse('all_invoices'))
    #return redirect('/voucher/invoices/')


@login_required
def all_invoices_search(request):
    if request.is_ajax():
        text = request.POST['text']
        result = watson.search(text,models=(Invoice.objects.filter(company=request.user.currently_activated_company), \
                                                   InvoiceParticular.objects.filter(invoice__company=request.user.currently_activated_company)))
        datas = []
        print request.user.currently_activated_company.id
        for item in result:
            if item.object is not None:
                temp = {}
                print item.object, " This is Item.Object"
                if type(item.object)== InvoiceParticular:
                    print "This is item.object.account", item.object.account
                    temp['title'] = item.object.account.name
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)
                if type(item.object) == Invoice:
                    temp['title'] = item.object.party.name
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)

        return HttpResponse(json.dumps(datas), mimetype="application/json")



@login_required
def purchase_voucher(request, id=None):
    from core.models import VoucherSetting
    from core.models import CompanySetting
    approved = 0
    try:
        voucher_setting = VoucherSetting.objects.get(company=request.user.currently_activated_company)
        company_setting = CompanySetting.objects.get(company=request.user.currently_activated_company)
    except CompanySetting.DoesNotExist:
        #TODO Add a flash message
        return redirect('/settings/company')
    if id:
        purchase_voucher_obj = get_object_or_404(PurchaseVoucher, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
        if purchase_voucher_obj.status == 'Approved':
            approved = 1
    else:
        purchase_voucher_obj = PurchaseVoucher(company=request.user.currently_activated_company)
        scenario = 'Create'
        purchase_voucher_obj.date = date.today()
        purchase_voucher_obj.due_date = date.today()
    form = PurchaseVoucherForm(instance=purchase_voucher_obj, company=request.user.currently_activated_company)
    purchase_voucher_data = PurchaseVoucherSerializer(purchase_voucher_obj).data

    if purchase_voucher_data['date']:
        purchase_voucher_data['date'] = purchase_voucher_data['date'].strftime("%m/%d/%Y")
    if purchase_voucher_data['due_date']:
        purchase_voucher_data['due_date'] = purchase_voucher_data['due_date'].strftime("%m/%d/%Y")
    purchase_voucher_data['read_only'] = {
        'purchase_voucher_prefix': voucher_setting.purchase_voucher_prefix,
        'purchase_voucher_suffix': voucher_setting.purchase_voucher_suffix,
    }
    return render(request, 'purchase_voucher.html', {'form': form, 'data': purchase_voucher_data, 'scenario': scenario, 'approved': approved})


@login_required
def save_purchase_voucher(request):
    params = json.loads(dict(request.POST.iterlists())['data'][0])
    dct = {'rows': {}}
    vch_no = params.get('voucher_no')
    try:
        vch_no = int(vch_no)
    except ValueError:
        dct['error_message'] = 'Only numbers are allowed in voucher no.'
        return HttpResponse(json.dumps(dct), mimetype='application/json')

    if params.get('id'):
        purchase_voucher_obj = PurchaseVoucher.objects.get(id=params.get('id'), company=request.user.currently_activated_company)
    else:
        purchase_voucher_obj = PurchaseVoucher(company=request.user.currently_activated_company)
        # if not created:
    try:
        existing = PurchaseVoucher.objects.get(voucher_no=params.get('voucher_no'), company=request.user.currently_activated_company)
        if purchase_voucher_obj.id is not existing.id:
            return HttpResponse(json.dumps({'error_message': 'Voucher No. already exists'}),
                                mimetype="application/json")
    except PurchaseVoucher.DoesNotExist:
        pass

    purchase_voucher_values = {'party_id': params.get('party'), 'voucher_no': params.get('voucher_no'),
                      'description': params.get('description'),
                      'reference': params.get('reference'),
                      'date': date(int(params.get('date').split('/')[2]), int(params.get('date').split('/')[0]),
                                   int(params.get('date').split('/')[1])),
                      'due_date': date(int(params.get('due_date').split('/')[2]), int(params.get('due_date').split('/')[0]),
                                   int(params.get('due_date').split('/')[1])),
                      'tax': params.get('tax'),
                      'currency_id': params.get('currency'), 'company': request.user.currently_activated_company, 'status': 'Unapproved',
                      'total_amount': params.get('total_amount')}

    if request.FILES:
        purchase_voucher_values['attachment'] = request.FILES['attachment']
    if purchase_voucher_values['total_amount'] == '':
        purchase_voucher_values['total_amount'] = 0
    purchase_voucher_obj = save_model(purchase_voucher_obj, purchase_voucher_values)
    dct['id'] = purchase_voucher_obj.id
    model = PurchaseParticular
    for index, row in enumerate(params['particulars']['rows']):
        if row.get('discount') == '':
            row['discount'] = 0
        values = {'sn': index + 1, 'account_id': row.get('account'), 'description': row.get('description'),
                  'unit_price': row.get('unit_price'), 'quantity': row.get('quantity'), 'discount': row.get('discount'),
                  'tax_scheme_id': row.get('tax_scheme'), 'purchase_voucher': purchase_voucher_obj}
        # print row.get('id')
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('particulars').get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def delete_purchase_voucher(request, id):
    try:
        obj = PurchaseVoucher.objects.get(id=id)
    except PurchaseVoucher.DoesNotExist:
        obj = None
    if obj:
        obj.particulars.all().delete()
        obj.delete()
    return redirect(reverse_lazy('new_purchase_voucher'))


@login_required
def list_purchase_vouchers(request):
    if request.method == "POST":
        search_text = request.POST.get('search-text')
        result = watson.search(search_text,models=(PurchaseVoucher.objects.filter(company=request.user.currently_activated_company), \
                                                   PurchaseParticular.objects.filter(purchase_voucher__company=request.user.currently_activated_company)))
        result_obj = [res.object for res in result]
        res = []
        for item in result_obj:
            if type(item) == PurchaseParticular:
                res.append(item.purchase_voucher)
            if type(item) == PurchaseVoucher:
                res.append(item)
        res = list(set(res))
        return render(request, 'list_purchase_voucher.html', {'objects': res})

    objects = PurchaseVoucher.objects.filter(company=request.user.currently_activated_company)
    return render(request, 'list_purchase_voucher.html', {'objects': objects})


@login_required
def search_purchase_vouchers(request):
   if request.is_ajax():
        text = request.POST['text']
        result = watson.search(text,models=(PurchaseVoucher.objects.filter(company=request.user.currently_activated_company), \
                                                   PurchaseParticular.objects.filter(purchase_voucher__company=request.user.currently_activated_company)))
        datas = []
        for item in result:
            if item.object is not None:
                temp = {}
                if type(item.object)== PurchaseParticular:
                    temp['title'] = item.object.account.name
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)
                if type(item.object) == PurchaseVoucher:
                    temp['title'] = item.object.party.name
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)

        return HttpResponse(json.dumps(datas), mimetype="application/json")



@group_required('Owner', 'SuperOwner', 'Supervisor')
def approve_purchase_voucher(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        voucher = PurchaseVoucher.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    status = voucher.backend_approve()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Owner', 'SuperOwner', 'Supervisor')
def unapprove_purchase_voucher(request, id):
    dct = {}
    try:
        voucher = PurchaseVoucher.objects.get(id=id, company=request.user.currently_activated_company)
    except:
        dct['error_message'] = 'Voucher can not be approved.'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    status = voucher.backend_unapprove()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def journal_voucher(request, id=None):
    approved = 0
    if id:
        voucher = get_object_or_404(JournalVoucher, id=id, company=request.user.currently_activated_company)
        voucher.date = voucher.date.strftime("%m/%d/%Y")
        scenario = 'Update'
    else:
        voucher = JournalVoucher(company=request.user.currently_activated_company, date=date.today().strftime("%m/%d/%Y"))
        scenario = 'Create'
    data = JournalVoucherSerializer(voucher).data
    # print data
    if voucher.status == 'Approved':
        approved = 1
        #objects = JournalVoucher.objects.filter(company=request.user.currently_activated_company)
        # return render(request, 'journal_voucher_approved.html', {'data': data})
    return render(request, 'journal_voucher.html', {'approved': approved, 'data': data, 'scenario': scenario})


@login_required
def cancel_journal_voucher(request):
    r = save_journal_voucher(request)
    dct = json.loads(r.content)
    obj = JournalVoucher.objects.get(id=dct.get('id'))
    obj.status = 'Cancelled'
    obj.save()
    return r

import os
from settings import MEDIA_ROOT

@login_required
def delete_journal_attachment(request, id):
    try:
        jv = JournalVoucher.objects.get(id=id, company=request.user.currently_activated_company)
        path = os.path.join(MEDIA_ROOT, str(jv.attachment))
        os.remove(path)
        jv.attachment = ''
        jv.save()
    except JournalVoucher.DoesNotExist:
        print 'File Does not Exist'
    return redirect(reverse_lazy('update_journal_voucher', kwargs={'id': id}))


@login_required
def delete_purchase_voucher_attachment(request, id):
    try:
        pv = PurchaseVoucher.objects.get(id=id, company=request.user.currently_activated_company)
        path = os.path.join(MEDIA_ROOT, str(pv.attachment))
        os.remove(path)
        pv.attachment = ''
        pv.save()
    except PurchaseVoucher.DoesNotExist:
        print 'File Does not Exist'
    return redirect(reverse_lazy('update_purchase_voucher', kwargs={'id': id}))

def empty_to_None(dict, list_of_attr):
    for attr in list_of_attr:
        if dict.get(attr) == '':
            dict[attr] = None
    return dict


@login_required
def list_journal_vouchers(request):
    objects = JournalVoucher.objects.filter(company=request.user.currently_activated_company)
    if request.method == "POST":
        search_text = request.POST.get('search-text')
        result = watson.search(search_text,models=(JournalVoucher.objects.filter(company=request.user.currently_activated_company), \
                                                   JournalVoucherRow.objects.filter(journal_voucher__company=request.user.currently_activated_company)))
        result_obj = [res.object for res in result]
        res = []
        for item in result_obj:
            if type(item) == JournalVoucherRow:
                res.append(item.journal_voucher)
            if type(item) == JournalVoucher:
                res.append(item)
        res = list(set(res))
        return render(request, 'list_journal_vouchers.html', {'objects': res})

    return render(request, 'list_journal_vouchers.html', {'objects': objects})


@login_required
def journals_search(request):
    if request.is_ajax():
        text = request.POST['text']
        result = watson.search(text,models=(JournalVoucher.objects.filter(company=request.user.currently_activated_company), \
                                                   JournalVoucherRow.objects.filter(journal_voucher__company=request.user.currently_activated_company)))
        datas = []
        for item in result:
            if item.object is not None:
                temp = {}
                if type(item.object) == JournalVoucherRow:
                    temp['title'] = item.object.account.name
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)
                if type(item.object) == JournalVoucher:
                    temp['title'] = "Journal Voucher at %s" % (item.object.date)
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)
        return HttpResponse(json.dumps(datas), mimetype="application/json")


@login_required
def save_journal_voucher(request):
    para = request.POST
    cont = para.get('continue')
    myDict = dict(para.iterlists())
    valu = myDict['data'][0]

    params = (json.loads(valu))

    if request.FILES:
        myfile = request.FILES

    else:
        myfile = None
    dct = {}
    res = params['date'].encode('utf-8').split('/')
    params['date'] = res[2] + '-' + res[0] + '-' + res[1]

    vch_no = params.get('voucher_no')
    try:
        vch_no = int(vch_no)
    except ValueError:
        dct['error_message'] = 'Only numbers are allowed in voucher no.'
        return HttpResponse(json.dumps(dct), mimetype='application/json')

    if params['id']:
        voucher = JournalVoucher.objects.get(id=params['id'])
        # scenario = 'create'
    else:
        voucher = JournalVoucher(company=request.user.currently_activated_company)
    try:
        existing = JournalVoucher.objects.get(voucher_no=params['voucher_no'], company=request.user.currently_activated_company)
        if voucher.id is not existing.id:
            return HttpResponse(json.dumps({'error_message': 'Voucher no. already exists'}),
                                mimetype="application/json")
    except JournalVoucher.DoesNotExist:
        pass
    voucher_values = {'date': params['date'], 'voucher_no': params['voucher_no'], 'status': 'Unapproved',
                      'narration': params['narration'], 'company': request.user.currently_activated_company}
    if myfile is not None:
        voucher_values['attachment'] = myfile['attachment']
    voucher = save_model(voucher, voucher_values)
    dct['id'] = voucher.id
    model = JournalVoucherRow

    for index, row in enumerate(params['journal_voucher']['rows']):
        if invalid(row, ['account']):
            continue
        empty_to_None(row, ['dr_amount', 'cr_amount'])
        if row['type'].lower() == 'dr':
            dr_amount = row['dr_amount']
            cr_amount = 0
        elif row['type'].lower() == 'cr':
            cr_amount = row['cr_amount']
            dr_amount = 0
        values = {'account_id': row['account'], 'dr_amount': dr_amount,
                  'cr_amount': cr_amount, 'type': row['type'],
                  'journal_voucher': voucher, 'description':row.get('description')}

        # if len(JournalVoucherRow.objects.all()) == 0:
        #     iid = row.get(id, 1)
        # else:
        #     iid = row.get(id, max(JournalVoucherRow.objects.values_list('id', flat=True)) + 1)

        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)

        if not created:
            submodel = save_model(submodel, values)
            # dct['rows'][index] = submodel.id
    delete_rows(params['journal_voucher']['deleted_rows'], model)
    # print params

    # cont = False
    if cont:
        dct = {'redirect_to': str(reverse_lazy('new_journal_voucher'))}
    else:
        dct = {'redirect_to': '/voucher/journal/' + str(voucher.id)}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Owner', 'SuperOwner', 'Supervisor')
def approve_journal_voucher(request):
    params = json.loads(request.body)
    dct = {'rows': []}
    if params.get('id'):
        voucher = JournalVoucher.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    for row in voucher.rows.all():
        if row.type == 'Dr':
            set_transactions(voucher, voucher.date,
                             ['dr', row.account, row.dr_amount],
            )
        else:
            set_transactions(voucher, voucher.date,
                             ['cr', row.account, row.cr_amount],
            )
        dct['rows'].append(row.id)

    voucher.status = 'Approved'
    voucher.save()
    dct['status'] = 'Approved'
    dct['redirect_to'] = '/voucher/journal/' + str(params.get('id'))
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def delete_journal_voucher(request, id):
    obj = get_object_or_404(JournalVoucher, id=id, company=request.user.currently_activated_company)
    ctype = ContentType.objects.get(model='journalvoucher')
    try:
        entries_to_be_deleted = JournalEntry.objects.filter(content_type=ctype, object_id=id)
        for entry_to_be_deleted in entries_to_be_deleted:
            for transaction_to_be_deleted in Transaction.objects.filter(journal_entry=entry_to_be_deleted):
                transaction_model = type(transaction_to_be_deleted)
                _transaction_delete(sender=transaction_model, instance=transaction_to_be_deleted)
            entry_to_be_deleted.delete()
    except:
        pass
    obj.delete()
    return redirect(reverse('list_journal_vouchers'))


@login_required
def unapprove_journal_voucher(request, id):
    obj = JournalVoucher.objects.get(company=request.user.currently_activated_company, id=id)
    ctype = ContentType.objects.get(model='journalvoucher')
    if obj.status == 'Approved':
        entries = JournalEntry.objects.filter(content_type=ctype, object_id=obj.id)

        for entry in entries:
            entry.delete()
        # obj.delete()
        obj.status = 'Unapproved'
        obj.save()

        return redirect('/voucher/journal/' + str(id))
    else:
        return redirect('/voucher/journal/' + str(id))

import os
from settings import MEDIA_ROOT
@login_required
def cash_receipt(request, id=None):
    approved = 0
    if id:
        receipt = get_object_or_404(CashReceipt, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
        receipt.date = receipt.date.strftime("%m/%d/%Y")
    else:
        receipt = CashReceipt(date=date.today().strftime('%m/%d/%Y'), company=request.user.currently_activated_company)
        scenario = 'New'
    if receipt.status == 'Approved':
        approved = 1
    form = CashReceiptForm(instance=receipt, company=request.user.currently_activated_company)

    receipt_data = CashReceiptSerializer(receipt).data

    return render(request, 'cash_receipt.html', {'approved':approved,'id':id, 'form': form, 'scenario': scenario, 'data': receipt_data})

# @transaction.commit_manually
@login_required
def save_cash_receipt(request):
    params = json.loads(dict(request.POST.iterlists())['data'][0])
    dct = {}

    vch_no = params.get('voucher_no')
    try:
        vch_no = int(vch_no)
    except ValueError:
        dct['error_message'] = 'Only numbers are allowed in voucher no.'
        return HttpResponse(json.dumps(dct), mimetype='application/json')

    if params.get('id'):
        cash = CashReceipt.objects.get(id=params.get('id'), company=request.user.currently_activated_company)
    else:
        cash = CashReceipt(company=request.user.currently_activated_company)

    try:
        existing = CashReceipt.objects.get(voucher_no=params.get('voucher_no'), company=request.user.currently_activated_company)
        if cash.id is not existing.id:
            return HttpResponse(json.dumps({'error_message': 'Voucher No. already exists'}),
                                mimetype="application/json")
    except CashReceipt.DoesNotExist:
        pass

    cash_values = {'voucher_no': params.get('voucher_no'), 'narration': params.get('narration'), \
                   'date': date(int(params.get('date').split('/')[2]), int(params.get('date').split('/')[0]),int(params.get('date').split('/')[1])),\
                   'cash_account_id': params.get('cash_account'), 'company': request.user.currently_activated_company, 'status': 'Unapproved' }
    if request.FILES:
        cash_values['attachment'] = request.FILES['attachment']

    cash = save_model(cash, cash_values)
    dct['id'] = cash.id
    model = CashReceiptRow
    for index, row in enumerate(params['particulars']['rows']):
        if invalid(row, ['amount']):
            continue
        from_account = Account.objects.filter(id=row.get('from_account'))[0]
        values = {'sn': index + 1, 'amount': row.get('amount'), 'from_account': from_account,
                  'reference_no': row.get('reference_no'), 'description': row.get('description'),
                  'cash_receipt': cash}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)

    delete_rows(params.get('particulars').get('deleted_rows'), model)

    dct['redirect_to'] = '/voucher/cash-receipt/' + str(dct['id'])
    return HttpResponse(json.dumps(dct), mimetype='application/json')

@login_required
def delete_cash_receipt(request, id=None):
    obj = get_object_or_404(CashReceipt, id=id, company=request.user.currently_activated_company)
    obj_rows = CashReceiptRow.objects.filter(cash_receipt=obj)
    ctype = ContentType.objects.get(model='cashreceiptrow')
    for item in obj_rows:
        if item.cash_receipt.status == 'Approved':
            entries = JournalEntry.objects.filter(content_type=ctype,object_id=item.id)
            for entry in entries:
                entry.delete()

    obj.delete()
    return redirect('/voucher/cash-receipt/')


@login_required
def deleted_cash_receipt(request,id=None):
    obj = get_object_or_404(CashReceipt, id=id, company=request.user.currently_activated_company)
    obj_rows = CashReceiptRow.objects.filter(cash_receipt=obj)
    ctype = ContentType.objects.get(model='cashreceiptrow')
    for item in obj_rows:
        if item.cash_receipt.status == 'Approved':
            entries = JournalEntry.objects.filter(content_type=ctype,object_id=item.id)
            for entry in entries:
                entry.delete()

    obj.delete()
    return redirect('/voucher/cash-receipts/')

@login_required
def list_cash_receipts(request):
    data_voucher = CashReceipt.objects.filter(company=request.user.currently_activated_company).order_by('-date')
    # data_row = [CashReceiptRow.objects.filter(cash_receipt=item) for item in data_voucher]
    if request.method == "POST":
        search_text = request.POST.get('search-text')
        result = watson.search(search_text,models=(CashReceipt.objects.filter(company=request.user.currently_activated_company), \
                                                   CashReceiptRow.objects.filter(cash_receipt__company=request.user.currently_activated_company)))
        result_obj = [res.object for res in result]
        res = []
        for item in result_obj:
            if type(item) == CashReceiptRow:
                res.append(item.cash_receipt)
            if type(item) == CashReceipt:
                res.append(item)
        res = list(set(res))
        return render(request, 'list_cash_receipts.html', {'data_voucher': res})
    return render(request, 'list_cash_receipts.html', {'data_voucher': data_voucher})


@login_required
def cash_receipts_search(request):
    if request.is_ajax():
        text = request.POST['text']
        result = watson.search(text,models=(CashReceipt.objects.filter(company=request.user.currently_activated_company), \
                                                   CashReceiptRow.objects.filter(cash_receipt__company=request.user.currently_activated_company)))
        datas = []
        for item in result:
            if item.object is not None:
                temp = {}
                if type(item.object)== CashReceiptRow:
                    temp['title'] = item.object.from_account.name
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)
                if type(item.object) == CashReceipt:
                    temp['title'] = item.object.cash_account.name
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)

        return HttpResponse(json.dumps(datas), mimetype="application/json")


@login_required
def cash_payment(request, id=None):
    approved = 0
    if id:
        receipt = get_object_or_404(CashPayment, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
        receipt.date = receipt.date.strftime("%m/%d/%Y")
    else:
        receipt = CashPayment(date=date.today().strftime('%m/%d/%Y'), company=request.user.currently_activated_company)
        scenario = 'New'
    if receipt.status == 'Approved':
        approved = 1
    form = CashPaymentForm(instance=receipt, company=request.user.currently_activated_company)

    receipt_data = CashPaymentSerializer(receipt).data

    return render(request, 'cash_payment.html', {'approved':approved,'id':id,'form': form, 'scenario': scenario, 'data': receipt_data})


@login_required
def save_cash_payment(request):
    params = json.loads(dict(request.POST.iterlists())['data'][0])
    dct = {}
    vch_no = params.get('voucher_no')
    try:
        vch_no = int(vch_no)
    except ValueError:
        dct['error_message'] = 'Only numbers are allowed in voucher no.'
        return HttpResponse(json.dumps(dct), mimetype='application/json')

    if params.get('id'):
        cash = CashPayment.objects.get(id=params.get('id'), company=request.user.currently_activated_company)
    else:
        cash = CashPayment(company=request.user.currently_activated_company)

    try:
        existing = CashPayment.objects.get(voucher_no=params.get('voucher_no'), company=request.user.currently_activated_company)
        if cash.id is not existing.id:
            return HttpResponse(json.dumps({'error_message': 'Voucher No. already exists'}),
                                mimetype="application/json")
    except CashPayment.DoesNotExist:
        pass

    cash_values = {'voucher_no': params.get('voucher_no'), 'narration': params.get('narration'), \
                   'date': date(int(params.get('date').split('/')[2]), int(params.get('date').split('/')[0]),int(params.get('date').split('/')[1])),\
                   'cash_account_id': params.get('cash_account'), 'company': request.user.currently_activated_company, 'status': 'Unapproved' }
    if request.FILES:
        cash_values['attachment'] = request.FILES['attachment']
    cash = save_model(cash, cash_values)
    dct['id'] = cash.id
    model = CashPaymentRow
    for index, row in enumerate(params['particulars']['rows']):
        if invalid(row, ['amount']):
            continue
        to_account = Account.objects.filter(id=row.get('to_account'))[0]
        values = {'sn': index + 1, 'amount': row.get('amount'), 'to_account': to_account,
                  'reference_no': row.get('reference_no'), 'description': row.get('description'),
                  'cash_payment': cash}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
    delete_rows(params.get('particulars').get('deleted_rows'), model)

    dct['redirect_to'] = '/voucher/cash-payment/' + str(dct['id'])
    return HttpResponse(json.dumps(dct), mimetype='application/json')

@login_required
def delete_cash_payment(request, id=None):
    obj = get_object_or_404(CashPayment, id=id, company=request.user.currently_activated_company)
    obj_rows = CashPaymentRow.objects.filter(cash_payment=obj)
    ctype = ContentType.objects.get(model='cashpaymentrow')
    for item in obj_rows:
        if item.cash_payment.status == 'Approved':
            entries = JournalEntry.objects.filter(content_type=ctype,object_id=item.id)
            for entry in entries:
                entry.delete()

    obj.delete()
    return redirect('/voucher/cash-payments/')


@login_required
def deleted_cash_payment(request,id=None):
    obj = get_object_or_404(CashPayment, id=id, company=request.user.currently_activated_company)
    obj_rows = CashPaymentRow.objects.filter(cash_payment=obj)
    ctype = ContentType.objects.get(model='cashpaymentrow')
    for item in obj_rows:
        if item.cash_payment.status == 'Approved':
            entries = JournalEntry.objects.filter(content_type=ctype,object_id=item.id)
            for entry in entries:
                entry.delete()

    obj.delete()
    return redirect('/voucher/cash-payments/')


@login_required
def list_cash_payments(request):
    data_voucher = CashPayment.objects.filter(company=request.user.currently_activated_company).order_by('-date')
    # data_row = [CashPaymentRow.objects.filter(cash_payment=item) for item in data_voucher]
    if request.method == "POST":
        search_text = request.POST.get('search-text')
        result = watson.search(search_text,models=(CashPayment.objects.filter(company=request.user.currently_activated_company), \
                                                   CashPaymentRow.objects.filter(cash_payment__company=request.user.currently_activated_company)))
        result_obj = [res.object for res in result]
        res = []
        for item in result_obj:
            if type(item) == CashPaymentRow:
                res.append(item.cash_payment)
            if type(item) == CashPayment:
                res.append(item)
        res = list(set(res))
        return render(request, 'list_cash_payments.html', {'data_voucher': res})

    return render(request, 'list_cash_payments.html', {'data_voucher': data_voucher})


@login_required
def cash_payments_search(request):
    if request.is_ajax():
        text = request.POST['text']
        result = watson.search(text,models=(CashPayment.objects.filter(company=request.user.currently_activated_company), \
                                                   CashPaymentRow.objects.filter(cash_payment__company=request.user.currently_activated_company)))
        datas = []
        for item in result:
            if item.object is not None:
                temp = {}
                if type(item.object)== CashPaymentRow:
                    temp['title'] = item.object.to_account.name
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)
                if type(item.object) == CashPayment:
                    temp['title'] = item.object.cash_account.name
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)

        return HttpResponse(json.dumps(datas), mimetype="application/json")


@login_required
def party_invoices(request, id):
    objs = Invoice.objects.filter(company=request.user.currently_activated_company, party=Party.objects.get(id=id), pending_amount__gt=0)
    lst = []
    for obj in objs:
        lst.append({'id': obj.id, 'bill_no': obj.invoice_no, 'date': obj.date, 'total_amount': obj.total_amount,
                    'pending_amount': obj.pending_amount, 'due_date': obj.due_date})
    return HttpResponse(json.dumps(lst, default=handler), mimetype="application/json")


# @login_required
# def save_cash_receipt(request):
#     params = json.loads(request.body)
#     dct = {'rows': {}}
#     res = params.get('receipt_on').encode('utf-8').split("/")
#     params['receipt_on'] = res[2]+'-'+res[0]+'-'+res[1]
#     #print params
#
#     # try:
#     if params.get('id'):
#         voucher = CashReceipt.objects.get(id=params.get('id'), company=request.user.currently_activated_company)
#     else:
#         voucher = CashReceipt(company=request.user.currently_activated_company)
#         # if not created:
#     try:
#         existing = CashReceipt.objects.get(voucher_no=params.get('voucher_no'), company=request.user.currently_activated_company)
#         if voucher.id is not existing.id:
#             return HttpResponse(json.dumps({'error_message': 'Voucher no. already exists'}),
#                                 mimetype="application/json")
#     except CashReceipt.DoesNotExist:
#         pass
#     values = {'party_id': params.get('party'), 'receipt_on': params.get('receipt_on'),
#               'voucher_no': params.get('voucher_no'),
#               'reference': params.get('reference'), 'company': request.user.currently_activated_company}
#     voucher = save_model(voucher, values)
#     dct['id'] = voucher.id
#     # except Exception as e:
#     #
#     #     if hasattr(e, 'messages'):
#     #         dct['error_message'] = '; '.join(e.messages)
#     #     else:
#     #         dct['error_message'] = 'Error in form data!'
#     model = CashReceiptRow
#     if params.get('table_vm').get('rows'):
#         for index, row in enumerate(params.get('table_vm').get('rows')):
#             if invalid(row, ['payment']) and invalid(row, ['discount']):
#                 continue
#             if (row.get('discount') == '') | (row.get('discount') is None):
#                 row['discount'] = 0
#             if (row.get('payment') == '') | (row.get('payment') is None):
#                 row['payment'] = 0
#             invoice = Invoice.objects.get(invoice_no=row.get('bill_no'), company=request.user.currently_activated_company)
#             values = {'discount': row.get('discount'), 'receipt': row.get('payment'),
#                       'cash_receipt': voucher,
#                       'invoice': invoice}
#             submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
#             if not created:
#                 submodel = save_model(submodel, values)
#             dct['rows'][index] = submodel.id
#         total = float(params.get('total_payment')) + float(params.get('total_discount'))
#         voucher.amount = total
#         voucher.status = 'Unapproved'
#         voucher.save()
#     else:
#         voucher.amount = params.get('amount')
#         voucher.status = 'Unapproved'
#         voucher.save()
#     if params.get('continue'):
#         dct = {'redirect_to': str(reverse_lazy('create_cash_receipt'))}
#     return HttpResponse(json.dumps(dct), mimetype="application/json")
#

# @login_required
# def cash_payment(request, id=None):
#     if id:
#         voucher = get_object_or_404(CashPayment, id=id, company=request.user.currently_activated_company)
#         voucher.payment_on = voucher.payment_on.strftime("%m/%d/%Y")
#         scenario = 'Update'
#     else:
#         voucher = CashPayment(company=request.user.currently_activated_company, payment_on=date.today().strftime("%m/%d/%Y"))
#         scenario = 'Create'
#     data = CashPaymentSerializer(voucher).data
#     if voucher.status =='Approved':
#        return render(request, 'cash_payment_approved.html', {'data': data})
#     return render(request, 'cash_payment.html', {'scenario': scenario, 'data': data})


@login_required
def party_purchase_vouchers(request, id):
    objs = PurchaseVoucher.objects.filter(company=request.user.currently_activated_company, party=Party.objects.get(id=id), pending_amount__gt=0)
    lst = []
    for obj in objs:
        lst.append({'id': obj.id, 'bill_no': obj.reference, 'date': obj.date, 'total_amount': obj.total_amount,
                    'pending_amount': obj.pending_amount, 'due_date': obj.due_date})
    return HttpResponse(json.dumps(lst, default=handler), mimetype="application/json")


# @login_required
# def save_cash_payment(request):
#     params = json.loads(request.body)
#     dct = {'rows': {}}
#     res = params.get('payment_on').encode('utf-8').split("/")
#     params['payment_on'] = res[2]+'-'+res[0]+'-'+res[1]
#
#     # try:
#     if params.get('id'):
#         voucher = CashPayment.objects.get(id=params.get('id'))
#     else:
#         voucher = CashPayment(company=request.user.currently_activated_company)
#     try:
#         existing = CashPayment.objects.get(voucher_no=params.get('voucher_no'),
#                company=request.user.currently_activated_company)
#         if voucher.id is not existing.id:
#             return HttpResponse(json.dumps({'error_message': 'Voucher no. already exists'}),
#                                 mimetype="application/json")
#     except CashPayment.DoesNotExist:
#         pass
#     values = {'party_id': params.get('party'), 'payment_on': params.get('payment_on'),
#               'voucher_no': params.get('voucher_no'),
#               'reference': params.get('reference'), 'company': request.user.currently_activated_company}
#     voucher = save_model(voucher, values)
#     dct['id'] = voucher.id
#     # except Exception as e:
#     #
#     #     if hasattr(e, 'messages'):
#     #         dct['error_message'] = '; '.join(e.messages)
#     #     else:
#     #         dct['error_message'] = 'Error in form data!'
#     model = CashPaymentRow
#     if params.get('table_vm').get('rows'):
#         for index, row in enumerate(params.get('table_vm').get('rows')):
#             if invalid(row, ['payment']) and invalid(row, ['discount']):
#                 continue
#             if (row.get('discount') == '') | (row.get('discount') is None):
#                 row['discount'] = 0
#             if (row.get('payment') == '') | (row.get('payment') is None):
#                 row['payment'] = 0
#             purchase_voucher = PurchaseVoucher.objects.get(id=row.get('id'),
#                       company=request.user.currently_activated_company)
#             values = {'discount': row.get('discount'), 'payment': row.get('payment'),
#                       'cash_payment': voucher,
#                       'purchase_voucher': purchase_voucher}
#             submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
#             if not created:
#                 submodel = save_model(submodel, values)
#             dct['rows'][index] = submodel.id
#         total = float(params.get('total_payment')) + float(params.get('total_discount'))
#         voucher.amount = total
#         voucher.status = 'Unapproved'
#         voucher.save()
#     else:
#         voucher.amount = params.get('amount')
#         voucher.status = 'Unapproved'
#         voucher.save()
#     if params.get('continue'):
#         dct = {'redirect_to': str(reverse_lazy('create_cash_payment'))}
#     return HttpResponse(json.dumps(dct), mimetype="application/json")
#

@group_required('SuperOwner', 'Owner', 'Supervisor')
def approve_cash_receipt(request):
    params = json.loads(request.body)
    dct = {}
    res = params.get('date').encode('utf-8').split("/")
    params['date'] = res[2] + '-' + res[0] + '-' + res[1]
    if params.get('id'):
        voucher = CashReceipt.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    # cash_account = Account.objects.get(id=params.get('cash_account'))
    # # benefactor = Account.objects.get(id=params.get('benefactor'))
    # for row in voucher.rows.all():
    #     from_account = Account.objects.get(id=row.from_account.id)
    #
    #     set_transactions(row, params.get('date'),
    #                      ['dr', cash_account, row.amount],
    #                      ['cr', from_account, row.amount],
    #     )
    # voucher.status = 'Approved'
    # voucher.save()
    voucher.backend_approve()
    dct['redirect_to'] = '/voucher/cash-receipt/' + str(params.get('id'))
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('SuperOwner', 'Owner', 'Supervisor')
def approve_cash_payment(request):
    params = json.loads(request.body)
    dct = {}
    res = params.get('date').encode('utf-8').split("/")
    params['date'] = res[2] + '-' + res[0] + '-' + res[1]
    if params.get('id'):
        voucher = CashPayment.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    # cash_account = Account.objects.get(id=params.get('cash_account'))
    # # benefactor = Account.objects.get(id=params.get('benefactor'))
    # for row in voucher.rows.all():
    #     to_account = Account.objects.get(id=row.to_account.id)
    #     set_transactions(row, params.get('date'),
    #                      ['cr', cash_account, row.amount],
    #                      ['dr', to_account, row.amount],
    #     )
    # voucher.status = 'Approved'
    # voucher.save()
    voucher.backend_approve()
    dct['redirect_to'] = '/voucher/cash-payment/' + str(params.get('id'))
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('SuperOwner', 'Owner', 'SuperVisor')
def unapprove_cash_receipt(request, id):
    if id:
        obj = get_object_or_404(CashReceipt, id=id, company=request.user.currently_activated_company)
        # obj_rows = CashReceiptRow.objects.filter(cash_receipt=obj)
        # ctype = ContentType.objects.get(model='cashreceiptrow')
        # for item in obj_rows:
        #     entries = JournalEntry.objects.filter(content_type=ctype,object_id=item.id)
        #     for entry in entries:
        #         entry.delete()
        # obj.status='Unapproved'
        # obj.save()
        obj.backend_unapprove()

    return redirect('/voucher/cash-receipt/'+str(id))


@group_required('SuperOwner', 'Owner', 'Supervisor')
def unapprove_cash_payment(request, id):
    if id:
        obj = get_object_or_404(CashPayment, id=id, company=request.user.currently_activated_company)
        obj.backend_unapprove()
    # obj_rows = CashPaymentRow.objects.filter(cash_payment=obj)
    # ctype = ContentType.objects.get(model='cashpaymentrow')
    # for item in obj_rows:
    #     entries = JournalEntry.objects.filter(content_type=ctype,object_id=item.id)
    #     for entry in entries:
    #         entry.delete()
    # obj.status='Unapproved'
    # obj.save()
    return redirect('/voucher/cash-payment/'+str(id))


@login_required
def list_fixed_assets(request):
    objs = FixedAsset.objects.filter(company=request.user.currently_activated_company)
    #filtered_items = InvoiceFilter(request.GET, queryset=objs, company=request.user.currently_activated_company)
    return render(request, 'list_fixed_assets.html', {'objects': objs})


@login_required
def fixed_asset(request, id=None):
    approved = 0
    if id:
        voucher = get_object_or_404(FixedAsset, id=id, company=request.user.currently_activated_company)
        voucher.date = voucher.date.strftime("%m/%d/%Y")
        scenario = 'Update'
    else:
        voucher = FixedAsset(date=date.today().strftime("%m/%d/%Y"), company=request.user.currently_activated_company)
        scenario = 'Create'
    data = FixedAssetSerializer(voucher).data
    fixed_asset_category = Category.objects.get(name='Fixed Assets', company=request.user.currently_activated_company)
    if voucher.status == 'Approved':
        approved = 1
    return render(request, 'fixed_asset.html',
                  {'scenario': scenario, 'approved': approved, 'data': data, 'fixed_asset_category': fixed_asset_category})


@login_required
def save_fixed_asset(request):
    params = json.loads(request.body)
    res = params.get('date').encode('utf-8').split("/")
    params['date'] = res[2] + '-' + res[0] + '-' + res[1]
    dct = {'rows1': {}, 'rows2': {}}
    if params.get('id'):
        voucher = FixedAsset.objects.get(id=params.get('id'))
    else:
        voucher = FixedAsset(company=request.user.currently_activated_company)
    try:
        existing = FixedAsset.objects.get(voucher_no=params.get('voucher_no'), company=request.user.currently_activated_company)
        if voucher.id is not existing.id:
            return HttpResponse(json.dumps({'error_message': 'Voucher no. already exists'}),
                                mimetype="application/json")
    except FixedAsset.DoesNotExist:
        pass
    voucher_values = {'date': params.get('date'), 'voucher_no': params.get('voucher_no'),
                      'description': params.get('description'), 'company': request.user.currently_activated_company, 'status': 'Unapproved',
                      'from_account_id': params.get('from_account'), 'reference': params.get('reference')}
    voucher = save_model(voucher, voucher_values)
    dct['id'] = voucher.id
    model = FixedAssetRow
    for index, row in enumerate(params.get('table_vm').get('rows')):
        if invalid(row, ['asset_ledger', 'amount']):
            continue
        values = {'asset_ledger_id': row.get('asset_ledger'), 'description': row.get('description'),
                  'amount': row.get('amount'), 'fixed_asset': voucher}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows1'][index] = submodel.id
    delete_rows(params.get('table_vm').get('deleted_rows'), model)
    model = AdditionalDetail
    for index, row in enumerate(params.get('additional_details').get('rows')):
        values = {'assets_code': row.get('assets_code'), 'assets_type': row.get('assets_type'),
                  'vendor_name': row.get('vendor_name'), 'vendor_address': row.get('vendor_address'),
                  'amount': row.get('amount'), 'useful_life': row.get('useful_life'),
                  'description': row.get('description'), 'warranty_period': row.get('warranty_period'),
                  'maintenance': row.get('maintenance')}
        if all_empty_in_dict(values):
            continue
        values['fixed_asset'] = voucher
        if row.get('amount') == '':
            values['amount'] = None
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows2'][index] = submodel.id
    delete_rows(params.get('additional_details').get('deleted_rows'), model)
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('create_fixed_asset'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def approve_fixed_asset(request):
    params = json.loads(request.body)
    res = params.get('date').encode('utf-8').split("/")
    params['date'] = res[2] + '-' + res[0] + '-' + res[1]
    dct = {}
    if params.get('id'):
        voucher = FixedAsset.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return render_to_response('fixed_asset.html', json.dumps(dct))
    # for row in voucher.rows.all():
    #     set_transactions(row, voucher.date,
    #                      ['dr', row.asset_ledger, row.amount],
    #                      ['cr', voucher.from_account, row.amount])
    # voucher.status = 'Approved'
    # voucher.save()
    voucher.backend_approve()
    return redirect('/voucher/fixed-asset/' + str(params.get('id')))


@login_required
def unapprove_fixed_asset(request):
    params = json.loads(request.body)
    res = params.get('date').encode('utf-8').split("/")
    params['date'] = res[2] + '-' + res[0] + '-' + res[1]
    dct = {}
    if params.get('id'):
        voucher = FixedAsset.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being unapproved!'
        return render_to_response('fixed_asset.html', json.dumps(dct))
    voucher.backend_unapprove()
    return redirect('/voucher/fixed-asset/' + str(params.get('id')))


@login_required
def delete_fixed_asset(request, id):
    try:
        obj = FixedAsset.objects.get(id=id, company=request.user.currently_activated_company)
        obj.delete()
        for item in obj.rows.all():
            item.delete()
    except FixedAsset.DoesNotExist:
        pass
    return redirect('/voucher/fixed-asset')

from itertools import chain


@login_required
def all_unapproved_vouchers(request):
    bank_payments = BankPayment.objects.filter(company=request.user.currently_activated_company, status="Unapproved")
    bank_deposits = BankDeposit.objects.filter(company=request.user.currently_activated_company, status="Unapproved")
    cash_payments = CashPayment.objects.filter(company=request.user.currently_activated_company, status="Unapproved")
    cash_receipts = CashReceipt.objects.filter(company=request.user.currently_activated_company, status="Unapproved")
    fixed_assets = FixedAsset.objects.filter(company=request.user.currently_activated_company, status="Unapproved")
    day_journals = DayJournal.objects.filter(company=request.user.currently_activated_company, status="Unapproved")
    journal_vouchers = JournalVoucher.objects.filter(company=request.user.currently_activated_company, status="Unapproved")
    invoices = Invoice.objects.filter(company=request.user.currently_activated_company, status="Unapproved")
    purchase_vouchers = PurchaseVoucher.objects.filter(company=request.user.currently_activated_company, status="Unapproved")
    individual_payroll_vouchers = IndividualPayroll.objects.filter(company=request.user.currently_activated_company, status="Unapproved")
    group_payroll_vouchers = GroupPayroll.objects.filter(company=request.user.currently_activated_company, status="Unapproved")
    all_vouchers = list(chain(bank_payments, bank_deposits, cash_payments, cash_receipts, fixed_assets, day_journals,\
                              journal_vouchers, invoices, purchase_vouchers, individual_payroll_vouchers, group_payroll_vouchers))
    return render(request, 'all_unapproved_vouchers.html', {'datas': sorted(all_vouchers, key=lambda obj: obj.date)})