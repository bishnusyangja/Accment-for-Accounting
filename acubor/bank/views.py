from datetime import date
import json
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response

from bank.models import BankAccount, BankDeposit, BankDepositRow, BankPaymentRow, BankPayment
from bank.forms import BankAccountForm, BankDepositForm, BankPaymentForm
from lib import invalid, save_model
from bank.serializers import BankDepositSerializer, BankPaymentSerializer
from ledger.models import Account, delete_rows, JournalEntry , Transaction, _transaction_delete
from ledger.serializers import AccountSerializer
from users.models import group_required
from django.contrib.contenttypes.models import ContentType
import watson
from django.db import transaction
import os
from settings import MEDIA_ROOT


@login_required
def bank_settings(request):
    items = BankAccount.objects.filter(company=request.user.currently_activated_company)
    return render(request, 'bank_settings.html', {'items': items})


@login_required
def list_bank_accounts(request):
    items = BankAccount.objects.filter(company=request.user.currently_activated_company)
    return render(request, 'list_bank_accounts.html', {'items': items})


@login_required
def delete_bank_account(request, id):
    obj = get_object_or_404(BankAccount, id=id, company=request.user.currently_activated_company)
    obj.delete()
    return redirect('/bank/accounts/')


@login_required
def bank_account_form(request, id=None):
    if id:
        bank_account = get_object_or_404(BankAccount, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
    else:
        bank_account = BankAccount()
        scenario = 'Create'
    if request.POST:
        form = BankAccountForm(data=request.POST, instance=bank_account)
        if form.is_valid():
            item = form.save(commit=False)
            item.company = request.user.currently_activated_company
            item.save()
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': AccountSerializer(item.account).data})
            return redirect('/bank/accounts/')
    else:
        form = BankAccountForm(instance=bank_account)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'bank_account_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })


@login_required
def bank_deposit(request,id=None):
    approved = 0
    if id:
        receipt = get_object_or_404(BankDeposit, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
        receipt.date = receipt.date.strftime("%m/%d/%Y")
    else:
        receipt = BankDeposit(date=date.today().strftime('%m/%d/%Y'), company=request.user.currently_activated_company)
        scenario = 'New'
    if receipt.status == 'Approved':
        approved = 1

    form = BankDepositForm(instance=receipt, company=request.user.currently_activated_company)

    receipt_data = BankDepositSerializer(receipt).data

    return render(request, 'bank_deposit.html', {'approved':approved,'form': form, 'scenario': scenario, 'data': receipt_data, 'id':id})



@login_required
def save_bank_deposit(request):
    params = json.loads(dict(request.POST.iterlists())['data'][0])
    dct = {}
    vch_no = params.get('voucher_no')
    try:
        vch_no = int(vch_no)
    except ValueError:
        dct['error_message'] = 'Only numbers are allowed in voucher no.'
        return HttpResponse(json.dumps(dct), mimetype='application/json')

    if params.get('id'):
        bank = BankDeposit.objects.get(id=params.get('id'), company=request.user.currently_activated_company)
    else:
        bank = BankDeposit(company=request.user.currently_activated_company)

    try:
        existing = BankDeposit.objects.get(voucher_no=params.get('voucher_no'), company=request.user.currently_activated_company)
        if bank.id is not existing.id:
            return HttpResponse(json.dumps({'error_message': 'Voucher No. already exists'}),
                                mimetype="application/json")
    except BankDeposit.DoesNotExist:
        pass

    bank_values = {'voucher_no': params.get('voucher_no'), 'narration': params.get('narration'), \
                   'date': date(int(params.get('date').split('/')[2]), int(params.get('date').split('/')[0]),int(params.get('date').split('/')[1])),\
                   'bank_account_id': params.get('bank_account'), 'company': request.user.currently_activated_company, 'status': 'Unapproved' }

    if request.FILES:
        bank_values['attachment'] = request.FILES['attachment']
    bank = save_model(bank, bank_values)
    dct['id'] = bank.id
    model = BankDepositRow
    for index, row in enumerate(params['particulars']['rows']):
        if invalid(row, ['amount']):
            continue
        from_account = Account.objects.filter(id=row.get('from_account'))[0]
        values = {'sn': index + 1, 'amount': row.get('amount'), 'from_account': from_account,
                  'reference_no': row.get('reference_no'), 'description': row.get('description'),
                  'bank_deposit': bank}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
    delete_rows(params.get('particulars').get('deleted_rows'), model)
    dct['redirect_to'] = '/bank/bank-deposit/update/' + str(dct['id'])

    return HttpResponse(json.dumps(dct), mimetype='application/json')

@login_required
def delete_bank_deposit_attachment(request, id):
    if id is not None:
        obj = BankDeposit.objects.get(company=request.user.currently_activated_company, id=id)
        obj.attachment = ""
        obj.save()
        return reverse_lazy('update_bank_deposit', kwargs = {'id': id})


@login_required
def bank_payment(request,id=None):
    approved = 0
    if id:
        receipt = get_object_or_404(BankPayment, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
        receipt.date = receipt.date.strftime("%m/%d/%Y")
    else:
        receipt = BankPayment(date=date.today().strftime('%m/%d/%Y'), company=request.user.currently_activated_company)
        scenario = 'New'
    if receipt.status == 'Approved':
        approved = 1
    form = BankPaymentForm(instance=receipt, company=request.user.currently_activated_company)

    receipt_data = BankPaymentSerializer(receipt).data
    return render(request, 'bank_payment.html', {'approved':approved,'id':id, 'form': form, 'scenario': scenario, 'data': receipt_data})


@login_required
def save_bank_payment(request):
    params = json.loads(dict(request.POST.iterlists())['data'][0])
    dct = {}

    vch_no = params.get('voucher_no')
    try:
        vch_no = int(vch_no)
    except ValueError:
        dct['error_message'] = 'Only numbers are allowed in voucher no.'
        return HttpResponse(json.dumps(dct), mimetype='application/json')

    if params.get('id'):
        bank = BankPayment.objects.get(id=params.get('id'), company=request.user.currently_activated_company)
    else:
        bank = BankPayment(company=request.user.currently_activated_company)

    try:
        existing = BankPayment.objects.get(voucher_no=params.get('voucher_no'), company=request.user.currently_activated_company)
        if bank.id is not existing.id:
            return HttpResponse(json.dumps({'error_message': 'Voucher No. already exists'}),
                                mimetype="application/json")
    except BankPayment.DoesNotExist:
        pass

    bank_values = {'voucher_no': params.get('voucher_no'), 'narration': params.get('narration'), \
                   'date': date(int(params.get('date').split('/')[2]), int(params.get('date').split('/')[0]),int(params.get('date').split('/')[1])),\
                   'bank_account_id': params.get('bank_account'), 'company': request.user.currently_activated_company, 'status': 'Unapproved' }
    if request.FILES:
        bank_values['attachment'] = request.FILES['attachment']
    bank = save_model(bank, bank_values)
    dct['id'] = bank.id
    model = BankPaymentRow
    for index, row in enumerate(params['particulars']['rows']):
        if invalid(row, ['amount']):
            continue
        to_account = Account.objects.filter(id=row.get('to_account'))[0]
        values = {'sn': index + 1, 'amount': row.get('amount'), 'to_account': to_account,
                  'reference_no': row.get('reference_no'), 'description': row.get('description'),
                  'bank_payment': bank}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
    delete_rows(params.get('particulars').get('deleted_rows'), model)

    dct['redirect_to'] = '/bank/bank-payment/update/' + str(dct['id'])
    return HttpResponse(json.dumps(dct), mimetype='application/json')


@login_required
def delete_bank_deposit(request, id):
    obj = get_object_or_404(BankDeposit, id=id, company=request.user.currently_activated_company)
    obj_rows = BankDepositRow.objects.filter(bank_deposit=obj)
    ctype = ContentType.objects.get(model='bankdepositrow')
    for item in obj_rows:
        entries = JournalEntry.objects.filter(content_type=ctype,object_id=item.id)
        for entry in entries:
            entry.delete()
    obj.delete()
    return redirect('/bank/bank-deposit/')

@login_required
def deleted_bank_deposit(request, id):
    obj = get_object_or_404(BankDeposit, id=id, company=request.user.currently_activated_company)
    obj_rows = BankDepositRow.objects.filter(bank_deposit=obj)
    ctype = ContentType.objects.get(model='bankdepositrow')
    for item in obj_rows:
        entries = JournalEntry.objects.filter(content_type=ctype,object_id=item.id)
        for entry in entries:
            entry.delete()
    obj.delete()
    return redirect('/bank/bank-deposits/')

@login_required
def delete_bank_payment(request, id):
    obj = get_object_or_404(BankPayment, id=id, company=request.user.currently_activated_company)
    obj_rows = BankPaymentRow.objects.filter(bank_payment=obj)
    ctype = ContentType.objects.get(model='bankpaymentrow')
    for item in obj_rows:
        entries = JournalEntry.objects.filter(content_type=ctype,object_id=item.id)
        for entry in entries:
            entry.delete()

    obj.delete()
    return redirect('/bank/bank-payments/')

@login_required
def deleted_bank_payment(request, id):
    obj = get_object_or_404(BankPayment, id=id, company=request.user.currently_activated_company)
    obj_rows = BankPaymentRow.objects.filter(bank_payment=obj)
    ctype = ContentType.objects.get(model='bankpaymentrow')
    for item in obj_rows:
        if item.bank_payment.status == 'Approved':
            entries = JournalEntry.objects.filter(content_type=ctype,object_id=item.id)
            for entry in entries:
                entry.delete()

    obj.delete()
    return redirect('/bank/bank-payments/')

@login_required
def list_bank_deposits(request):
    data_voucher = BankDeposit.objects.filter(company=request.user.currently_activated_company).order_by('-date')
    # data_row = [BankDepositRow.objects.filter(bank_deposit=item) for item in data_voucher]
    if request.method == "POST":
        search_text = request.POST.get('search-text')
        result = watson.search(search_text,models=(BankDeposit.objects.filter(company=request.user.currently_activated_company), \
                                                   BankDepositRow.objects.filter(bank_deposit__company=request.user.currently_activated_company)))
        result_obj = [res.object for res in result]
        res = []
        for item in result_obj:
            if type(item) == BankDepositRow:
                res.append(item.bank_deposit)
            if type(item) == BankDeposit:
                res.append(item)
        res = list(set(res))
        return render(request, 'list_bank_deposits.html', {'data_voucher': res})

    return render(request, 'list_bank_deposits.html', {'data_voucher': data_voucher})


@login_required
def bank_deposits_search(request):
    if request.is_ajax():
        text = request.POST['text']
        result = watson.search(text,models=(BankDeposit.objects.filter(company=request.user.currently_activated_company), \
                                                   BankDepositRow.objects.filter(bank_deposit__company=request.user.currently_activated_company)))
        datas = []
        for item in result:
            if item.object is not None:
                temp = {}
                if type(item.object)== BankDepositRow:
                    temp['title'] = item.object.from_account.name
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)
                if type(item.object) == BankDeposit:
                    temp['title'] = item.object.bank_account.name
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)
        return HttpResponse(json.dumps(datas), mimetype="application/json")


@login_required
def list_bank_payments(request):
    data_voucher = BankPayment.objects.filter(company=request.user.currently_activated_company).order_by('-date')
    # data_row = [BankPaymentRow.objects.filter(bank_payment=item) for item in data_voucher]
    if request.method == "POST":
        search_text = request.POST.get('search-text')
        result = watson.search(search_text,models=(BankPayment.objects.filter(company=request.user.currently_activated_company), \
                                                   BankPaymentRow.objects.filter(bank_payment__company=request.user.currently_activated_company)))
        result_obj = [res.object for res in result]
        res = []
        for item in result_obj:
            if type(item) == BankPaymentRow:
                res.append(item.bank_payment)
            if type(item) == BankPayment:
                res.append(item)
        res = list(set(res))
        return render(request, 'list_bank_payments.html', {'data_voucher': res})

    return render(request, 'list_bank_payments.html', {'data_voucher': data_voucher})


@login_required
def bank_payments_search(request):
    if request.is_ajax():
        text = request.POST['text']
        result = watson.search(text,models=(BankPayment.objects.filter(company=request.user.currently_activated_company), \
                                                   BankPaymentRow.objects.filter(bank_payment__company=request.user.currently_activated_company)))
        datas = []
        for item in result:
            if item.object is not None:
                temp = {}
                if type(item.object)== BankPaymentRow:
                    temp['title'] = item.object.to_account.name
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)
                if type(item.object) == BankPayment:
                    temp['title'] = item.object.bank_account.name
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)
        return HttpResponse(json.dumps(datas), mimetype="application/json")


@group_required('SuperOwner', 'Owner', 'Supervisor')
def approve_bank_deposit(request):
    params = json.loads(request.body)
    res = params.get('date').encode('utf-8').split("/")
    params['date'] = res[2] + '-' + res[0] + '-' + res[1]
    dct = {}
    if params.get('id'):
        voucher = BankDeposit.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return render_to_response('fixed_asset.html', json.dumps(dct))
    voucher.backend_approve()
    dct['redirect_to'] = '/bank/bank-deposit/update/' + str(params.get('id'))
    # return redirect('/bank/bank-deposit/update/' + str(params.get('id')))
    return HttpResponse(json.dumps(dct), mimetype='application/json')


@login_required
def unapprove_bank_deposit(request, id):
    obj = get_object_or_404(BankDeposit, id=id, company=request.user.currently_activated_company)
    obj_rows = BankDepositRow.objects.filter(bank_deposit=obj)
    ctype = ContentType.objects.get(model='bankdepositrow')
    for item in obj_rows:
        entries = JournalEntry.objects.filter(content_type=ctype,object_id=item.id)
        for entry in entries:
            entry.delete()
    obj.status='Unapproved'
    obj.save()
    return redirect('/bank/bank-deposit/update/'+str(id))


@group_required('SuperOwner', 'Owner', 'Supervisor')
def approve_bank_payment(request):
    params = json.loads(request.body)
    res = params.get('date').encode('utf-8').split("/")
    params['date'] = res[2] + '-' + res[0] + '-' + res[1]
    dct = {}
    if params.get('id'):
        voucher = BankPayment.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return render_to_response('fixed_asset.html', json.dumps(dct))
    voucher.backend_approve()
    dct['redirect_to'] = '/bank/bank-payment/update/' + str(params.get('id'))
    return HttpResponse(json.dumps(dct), mimetype='application/json')


@login_required
def unapprove_bank_payment(request, id):
    obj = get_object_or_404(BankPayment, id=id, company=request.user.currently_activated_company)
    obj_rows = BankPaymentRow.objects.filter(bank_payment=obj)
    ctype = ContentType.objects.get(model='bankpaymentrow')
    for item in obj_rows:
        entries = JournalEntry.objects.filter(content_type=ctype,object_id=item.id)
        for entry in entries:
            entry.delete()
    obj.status='Unapproved'
    obj.save()
    return redirect('/bank/bank-payment/update/'+str(id))


@login_required
def bank_book(request, id):
    bank_account = BankAccount.objects.get(id=id)
    account = bank_account.account
    journal_entries = JournalEntry.objects.filter(transactions__account_id=account.id).order_by('id',
                                                                                                'date') \
        .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
    return render(request, 'bank_book.html',
                  {'account': account, 'bank_account': bank_account, 'journal_entries': journal_entries})
