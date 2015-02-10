from datetime import date
import json
from django.db import transaction
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType

from dayjournal.models import DayJournal, CashSales, CardSales, LottoDetail, BankAttachment, OtherAttachment, \
    CashEquivalentSales, SummaryInventory, SummaryTransfer, InventoryFuel, SalesAttachment, PurchaseAttachment, \
    VendorPayout, OtherPayout, VendorCharge, Deposits
from ledger.models import Account, set_transactions, delete_rows, Category, JournalEntry, Transaction, \
    _transaction_delete
from inventory.models import InventoryAccount, Category as InventoryCategory, Item, InventoryLedger
from dayjournal.serializers import DayJournalSerializer, LottoDetailSerializer
from lib import invalid, save_model, all_empty, add, zero_for_none, validate_row
from users.models import group_required
from dayjournal.filters import DayjournalFilter
import watson


@login_required
def all_day_journals(request):
    objects = DayJournal.objects.filter(company=request.user.currently_activated_company).order_by('date')
    # print objec
    return render(request, 'all_day_journals.html', {'objects': objects})


@login_required
def all_day_journals_improvised(request, year=date.today().year):
    year_list = DayJournal.objects.filter(company=request.user.currently_activated_company).values_list('date', flat=True)
    year_list = sorted(list(set([x.year for x in year_list])))[::-1]
    objects = DayJournal.objects.filter(company=request.user.currently_activated_company, date__year=year).order_by('date')
    # filtered_items = DayjournalFilter(request.GET, queryset=objects)
    filtered = [[item.date, item.voucher_no, item.status] for item in objects]
    fuel_sales_total, total_fuel_sales_total = [], []  # fuel total
    inside_sales_total, total_inside_sales_total = [], []  # inside total
    day_sales_total, total_day_sales_total = [], []  # total of the dayjournal
    lotto = []  # lotto total
    scratch_off_tot = []  # scratchoff total
    transfer_remit, transfer_remit_total = [], []  # Transfer Remittance
    lotto_scratchoff_total, total_lotto_scratchoff_total = [], []  # TOTAL OF LOTTO AND SCRATCH OFF
    sales_total = []  # total of sales in dayjournal
    tax, total_tax = [], []
    distribution_total, total_distribution_total = [], []
    distribution_other_cash, total_distribution_other_cash = [], []
    distribution_cash, total_distribution_cash = [], []
    cash_equivalents = []
    sales_card = []
    vendor_paidout, total_vendor_paidout = [], []
    other_paidout, total_other_paidout = [], []
    deposit_paidout, total_deposit_paidout = [], []
    paidout_total, total_paidout_total = [], []

    for item in objects:
        # INSIDE SALES
        if item.lotto_sales_dispenser_amount is None or item.lotto_sales_dispenser_amount == 0:
            lotto_amount = 0
        else:
            lotto_amount = item.lotto_sales_dispenser_amount
        lotto.append(lotto_amount)

        scratch_off_total = 0
        tot_scr = 0
        try:
            # print item.date
            scratch_off = ScratchOffLatest.objects.filter(date=item.date, company=request.user.currently_activated_company).order_by('-date')
            if scratch_off:
                for sc in scratch_off:
                    tot_scr += sc.grand_total()
                # tot_scr = scratch_off[0].grand_total()
            else:
                tot_scr = 0
        except ScratchOffLatest.DoesNotExist:
            pass
        # print tot_scr
        # for scratch_off in item.lotto_detail.all():
        #     print scratch_off
        #     day_close = scratch_off.day_close
        #     if day_close == 0:
        #         day_close = scratch_off.pack_count
        #     sales = (scratch_off.pack_count * zero_for_none(scratch_off.addition) + (
        #         day_close - scratch_off.day_open)) * zero_for_none(scratch_off.rate)
        #     scratch_off_total += sales
        # if scratch_off_total == 0:
        #     scratch_off_total = 0
        scratch_off_tot.append(tot_scr)

        tot_sale = 0
        sales_list = CashSales.objects.filter(day_journal=item)
        if len(sales_list) == 0:
            sales_total.append(0)
        else:
            for sale in sales_list:
                tot_sale += sale.amount
            sales_total.append(tot_sale)
        # END INSIDE SALES

        # TRANSFER REMITTANCE
        transfers = SummaryTransfer.objects.filter(day_journal=item)
        totl = 0
        if len(transfers) == 0:
            transfer_remit.append(0)
        else:
            for remit in transfers:
                totl += remit.cash
            transfer_remit.append(totl)

        # FUEL SALES
        tot = 0
        fuels = CashSales.objects.filter(day_journal=item, sales_ledger__name="Fuel Sales")
        if len(fuels) == 0:
            fuel_sales_total.append(0)
        else:
            for fuel in fuels:
                tot += fuel.amount
            fuel_sales_total.append(tot)
        #END FUEL SALES

        #TAX CALCULATION
        total_tax = 0
        for cash_sale in item.cash_sales.all():
            try:
                tax_rate = cash_sale.sales_ledger.tax_detail.all()[0].pri_tax_scheme.percent or 0
            except IndexError:
                tax_rate = 0
            except:
                tax_rate = 0
            tax_amount = cash_sale.amount * zero_for_none(tax_rate) / 100
            total_tax += tax_amount
        lotto_sales_ledger = Account.objects.get(name='Lotto Sales', company=request.user.currently_activated_company)
        try:
            lotto_tax_rate = lotto_sales_ledger.tax_detail.all()[0].pri_tax_scheme.percent
        except IndexError:
            lotto_tax_rate = 0
        lotto_tax = lotto_amount * zero_for_none(lotto_tax_rate) / 100
        total_tax += lotto_tax

        scratch_off_ledger = Account.objects.get(name='Scratch Off Sales', company=request.user.currently_activated_company)
        try:
            scratch_off_tax_rate = scratch_off_ledger.tax_detail.all()[0].pri_tax_scheme.percent
        except IndexError:
            scratch_off_tax_rate = 0
        scratch_off_tax = scratch_off_total * zero_for_none(scratch_off_tax_rate) / 100
        total_tax += scratch_off_tax
        tax.append(total_tax)
        #END TAX CALCULATION

        #START DISTRIBUTION CALCULATION
        tot2 = 0
        sales_thro_card = CardSales.objects.filter(day_journal=item)
        if len(sales_thro_card) == 0:
            sales_card.append(0)
        else:
            for its in sales_thro_card:
                tot2 += its.amount
            sales_card.append(tot2)

        eq_cash = CashEquivalentSales.objects.filter(day_journal=item)
        tot3 = 0
        if len(eq_cash) == 0:
            cash_equivalents.append(0)
        else:
            for ite in eq_cash:
                tot3 += ite.amount
            cash_equivalents.append(tot3)
        # END DISTRIBUTION CALCULATION

        #START PAIDOUTS
        tot4 = 0
        vendor = VendorPayout.objects.filter(day_journal=item)
        if len(vendor) == 0:
            vendor_paidout.append(0)
        else:
            for vend in vendor:
                tot4 += vend.amount
            vendor_paidout.append(tot4)

        tot5 = 0
        other = OtherPayout.objects.filter(day_journal=item)

        if len(other) == 0:
            other_paidout.append(0)
        else:
            for oth in other:
                tot5 += oth.amount
            other_paidout.append(tot5)

        tot6 = 0
        deposits = Deposits.objects.filter(day_journal=item)
        if len(deposits) == 0:
            deposit_paidout.append(0)
        else:
            for dep in deposits:
                tot6 += dep.amount
            deposit_paidout.append(tot6)

            #END VENDOR
    # SCRATCH OFF AND LOTTO TOTAL CALCULATION
    for i in range(len(scratch_off_tot)):
        res = lotto[i] + scratch_off_tot[i]
        lotto_scratchoff_total.append(res)

    for i in range(len(sales_total)):
        temp1 = sales_total[i] - fuel_sales_total[i]
        temp2 = sales_total[i] + lotto_scratchoff_total[i] + transfer_remit[i]
        temp3 = temp2 + tax[i]
        temp4 = cash_equivalents[i] + sales_card[i]
        temp5 = temp3 - temp4
        temp6 = vendor_paidout[i] + other_paidout[i] + deposit_paidout[i]
        inside_sales_total.append(temp1)
        day_sales_total.append(temp2)
        distribution_total.append(temp3)
        distribution_other_cash.append(temp4)
        distribution_cash.append(temp5)
        paidout_total.append(temp6)

    # Total of TOTALS
    total_fuel_sales_total = sum(fuel_sales_total)
    total_inside_sales_total = sum(inside_sales_total)
    total_day_sales_total = sum(day_sales_total)
    total_lotto_scratchoff_total = sum(lotto_scratchoff_total)
    transfer_remit_total = sum(transfer_remit)
    total_distribution_total = sum(distribution_total)
    total_distribution_cash = sum(distribution_cash)
    total_distribution_other_cash = sum(distribution_other_cash)
    total_tax = sum(tax)
    total_vendor_paidout = sum(vendor_paidout)
    total_other_paidout = sum(other_paidout)
    total_deposit_paidout = sum(deposit_paidout)
    total_paidout_total = sum(paidout_total)

    mydata = {}
    mydata['objects'] = objects
    mydata['fuel_sales_total'] = fuel_sales_total
    mydata['lotto_scratchoff_total'] = lotto_scratchoff_total
    mydata['transfer_remit'] = transfer_remit
    mydata['inside_sales_total'] = inside_sales_total
    mydata['day_sales_total'] = day_sales_total
    mydata['tax'] = tax
    mydata['distribution_total'] = distribution_total
    mydata['distribution_other_cash'] = distribution_other_cash
    mydata['distribution_cash'] = distribution_cash
    mydata['vendor_paidout'] = vendor_paidout
    # TOTALS OF TOTAL ARE HERE
    mydata['total_fuel_sales_total'] = total_fuel_sales_total
    mydata['total_inside_sales_total'] = total_inside_sales_total
    mydata['total_lotto_scratchoff_total'] = total_lotto_scratchoff_total
    mydata['transfer_remit_total'] = transfer_remit_total
    mydata['total_day_sales_total'] = total_day_sales_total
    mydata['total_distribution_cash'] = total_distribution_cash
    mydata['total_distribution_other_cash'] = total_distribution_other_cash
    mydata['total_distribution_total'] = total_distribution_total
    mydata['total_tax'] = total_tax
    mydata['total_vendor_paidout'] = total_vendor_paidout
    mydata['filtered_items'] = objects
    mydata['filtered'] = filtered
    mydata['total_other_paidout'] = total_other_paidout
    mydata['total_deposit_paidout'] = total_deposit_paidout
    mydata['other_paidout'] = other_paidout
    mydata['deposit_paidout'] = deposit_paidout
    mydata['paidout_total'] = paidout_total
    mydata['total_paidout_total'] = total_paidout_total

    # DATA LIST
    myli = find_li(mydata['filtered'])
    dat = []
    dat.append(mydata['objects'])
    dat.append(makelist(mydata['fuel_sales_total'], myli))
    dat.append(makelist(mydata['inside_sales_total'], myli))
    dat.append(makelist(mydata['day_sales_total'], myli))
    dat.append(makelist(mydata['tax'], myli))
    dat.append(makelist(mydata['distribution_total'], myli))
    dat.append(makelist(mydata['distribution_other_cash'], myli))
    dat.append(makelist(mydata['distribution_cash'], myli))
    dat.append(makelist(mydata['vendor_paidout'], myli))
    # TOTALS
    dat.append(makelist(mydata['total_fuel_sales_total'], myli))
    dat.append(makelist(mydata['total_inside_sales_total'], myli))
    dat.append(makelist(mydata['total_day_sales_total'], myli))
    dat.append(makelist(mydata['total_distribution_cash'], myli))
    dat.append(makelist(mydata['total_distribution_other_cash'], myli))
    dat.append(makelist(mydata['total_distribution_total'], myli))
    dat.append(makelist(mydata['total_tax'], myli))
    dat.append(makelist(mydata['total_vendor_paidout'], myli))
    dat.append(makelist(mydata['filtered'], myli))

    dat.append(makelist(mydata['lotto_scratchoff_total'], myli))
    dat.append(makelist(mydata['total_lotto_scratchoff_total'], myli))
    dat.append(makelist(mydata['transfer_remit'], myli))
    dat.append(makelist(mydata['transfer_remit_total'], myli))
    dat.append(makelist(mydata['filtered_items'], myli))
    dat.append(makelist(mydata['other_paidout'], myli))
    dat.append(makelist(mydata['deposit_paidout'], myli))
    dat.append(makelist(mydata['total_other_paidout'], myli))
    dat.append(makelist(mydata['total_deposit_paidout'], myli))
    dat.append(makelist(mydata['paidout_total'], myli))
    dat.append(makelist(mydata['total_paidout_total'], myli))

    return render(request, 'all_day_journal_improvised.html', {'dat': dat, 'year_list': year_list})


@login_required
def delete_day_journal(request, journal_date):
    obj = DayJournal.objects.get(company=request.user.currently_activated_company, date=journal_date)
    if obj.status == 'Approved':
        entries = JournalEntry.objects.filter(content_type__app_label='dayjournal', date=journal_date)

        for entry in entries:
            entry.delete()

    obj.delete()
    # obj.save()
    date = str(journal_date).split("-")
    return redirect('/day/journals2/' + date[0])


@login_required
def day_journal(request, journal_date=None):
    approved = 0
    if not journal_date:
        journal_date = date.today().strftime("%Y-%m-%d")
    try:
        dat = journal_date.encode('utf-8').split("-")
        tdat = date(int(dat[0]), int(dat[1]), int(dat[2]))
        day_journal = DayJournal.objects.get(date=tdat, company=request.user.currently_activated_company)

    except DayJournal.DoesNotExist:
        day_journal = DayJournal(date=tdat, company=request.user.currently_activated_company, cheque_deposit=0,
                                 cash_deposit=0, cash_withdrawal=0, cash_actual=0)
    day_journal_data = DayJournalSerializer(day_journal).data
    base_template = 'dashboard.html'
    if day_journal.status == 'Approved':
        approved = 1
    dct = {
        'approved': approved,
        'day_journal': day_journal_data,
        'base_template': base_template,
        'sales_attachments': day_journal.sales_attachments.all(),
        'purchase_attachments': day_journal.purchase_attachments.all(),
        'bank_attachments': day_journal.bank_attachments.all(),
        'other_attachments': day_journal.other_attachments.all(),
        'purchase_category': Category.objects.get(name='Purchase', company=request.user.currently_activated_company),
        'sales_category': Category.objects.get(name='Sales', company=request.user.currently_activated_company),
        'transfer_category': Category.objects.get(name='Transfer and Remittance', company=request.user.currently_activated_company),
    }

    if request.user.currently_activated_company.settings.company_type in ['Gas Station and Store', 'Gas Station', ]:
        dct['fuel_and_gas'] = InventoryCategory.objects.get(name='Fuel and Gas', company=request.user.currently_activated_company)

    return render(request, 'day_journal.html', dct)


@login_required
def get_journal(request):
    params = json.loads(request.body)
    try:
        journal, created = DayJournal.objects.get_or_create(date=params.get('day_journal_date'),
                                                            company=request.user.currently_activated_company, defaults={'voucher_no': params.get(
                'voucher_no'),
                                                                                               'cheque_deposit': 0,
                                                                                               'cash_deposit': 0,
                                                                                               'cash_withdrawal': 0,
                                                                                               'cash_actual': 0})
    except Exception as e:
        return {'error': 'Voucher No. already exists!'}
    if not created:
        journal.voucher_no = params.get('voucher_no')
        try:
            journal.save()
        except Exception as e:
            return {'error': 'Voucher No. already exists!'}
    return journal


# @login_required
# def save_cash_sales(request):
#     params = json.loads(request.body)
#     dct = {'invalid_attributes': {}, 'saved': {}}
#     model = CashSales
#     day_journal = get_journal(request)
#
#     if type(day_journal) == dict:
#         return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
#     for index, row in enumerate(params.get('rows')):
#         invalid_attrs = invalid(row, ['account_id', 'amount'])
#         if invalid_attrs:
#             dct['invalid_attributes'][index] = invalid_attrs
#             continue
#         values = {'sn': index + 1, 'sales_ledger_id': row.get('account_id'), 'amount': row.get('amount'),
#                   'day_journal': day_journal}
#         already_existing = CashSales.objects.filter(day_journal=day_journal, sales_ledger__id=values['sales_ledger_id'])
#         if len(already_existing) == 0:
#             submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
#             if row.get('tax_rate') is None:
#                 row['tax_rate'] = 0
#             if not created:
#                 submodel = save_model(submodel, values)
#             dct['saved'][index] = submodel.id
#     delete_rows(params.get('deleted_rows'), model)
#     day_journal.status = 'Unapproved'
#     day_journal.save()
#     return HttpResponse(json.dumps(dct), mimetype="application/json")

@login_required
def save_cash_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashSales
    day_journal = get_journal(request)

    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    if validate_row(params.get('rows'), 'account_id'):
        for index, row in enumerate(params.get('rows')):
            invalid_attrs = invalid(row, ['account_id', 'amount'])
            if invalid_attrs:
                dct['invalid_attributes'][index] = invalid_attrs
                continue
            values = {'sn': index + 1, 'sales_ledger_id': row.get('account_id'), 'amount': row.get('amount'),
                      'day_journal': day_journal}
            submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
            if row.get('tax_rate') is None:
                row['tax_rate'] = 0
            if not created:
                submodel = save_model(submodel, values)
            dct['saved'][index] = submodel.id
        delete_rows(params.get('deleted_rows'), model)
        day_journal.status = 'Unapproved'
        day_journal.save()
    else:
        dct['msg'] = 'Duplicate Particulars are not allowed.'
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_summary_sales_tax(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['register'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        day_journal = get_journal(request)
        if type(day_journal) == dict:
            return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
        try:
            day_journal.sales_tax = row.get('register')
            day_journal.status = 'Unapproved'
            day_journal.save()
            dct['saved'][0] = day_journal.id
        except:
            pass
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_summary_cash(request):
    params = json.loads(request.body)
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    if params.get('rows')[0].get('actual') == "" or None:
        params['rows'][0]['actual'] = 0
    day_journal.cash_actual = params.get('rows')[0].get('actual')
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps({'saved': {'0': 1}}), mimetype="application/json")


@login_required
def save_summary_transfer(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = SummaryTransfer
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    cash_account = Account.objects.get(name='Cash Account', company=request.user.currently_activated_company)
    for index, row in enumerate(params.get('rows')):
        if all_empty(row, ['cash']):
            continue
        for attr in ['cash']:
            if row.get(attr) is None or row.get(attr) == '':
                row[attr] = None
        values = {'sn': index + 1, 'transfer_type_id': row.get('transfer_type'), 'cash': row.get('cash'),
                  'commission': row.get('commission'), 'day_journal': day_journal}
        if values['commission'] is None or values['commission'] == '':
            values['commission'] = 0
        if float(values['commission']) > float(values['cash']):
            return HttpResponse(json.dumps({'error_message': "Commission cannot be greater than Cash"}), mimetype="application/json")
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id

    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_summary_inventory(request, fuel=False):
    params = json.loads(request.body)
    # print params
    dct = {'invalid_attributes': {}, 'saved': {}}
    if fuel:
        model = InventoryFuel
    else:
        model = SummaryInventory
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['item_id'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        purchase = row.get('purchase')
        sales = row.get('sales')
        actual = row.get('actual')
        if purchase is None or purchase == '':
            purchase = 0.0
        if sales is None or sales == '':
            sales = 0.0
        if actual is None or actual == '':
            actual = 0.0
        values = {'sn': index + 1, 'purchase': float(purchase), 'particular_id': row.get('item_id'),
                  'sales': float(sales), 'actual': float(actual), 'day_journal': day_journal}

        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)

        if not created:
            submodel = save_model(submodel, values)
        item = Item.objects.get(id=row.get('item_id'))
        item.current_stock = float(actual)
        item.save()
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_inventory_fuel(request):
    return save_summary_inventory(request, fuel=True)


@login_required
def save_lotto_detail(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = LottoDetail
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['rate', 'pack_count', 'day_open', 'day_close', 'addition'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'rate': row.get('rate'), 'pack_count': row.get('pack_count'),
                  'day_open': row.get('day_open'), 'day_close': row.get('day_close'),
                  'addition': row.get('addition'), 'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    scratch_off_sales_manual = params.get('scratch_off_sales_manual')
    if scratch_off_sales_manual == '':
        scratch_off_sales_manual = None
    day_journal.scratch_off_sales_manual = scratch_off_sales_manual
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_card_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CardSales
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    index = 0
    row = params.get('rows')[index]
    invalid_attrs = invalid(row, ['amount'])
    if invalid_attrs:
        dct['invalid_attributes'][index] = invalid_attrs
    temp = row.get('commission_out')
    if temp == '':
        temp = 0
    values = {'amount': row.get('amount'), 'commission_out': temp,
              'day_journal': day_journal}

    submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
    if not created:
        submodel = save_model(submodel, values)
    dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)

    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_cash_equivalent_sales(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = CashEquivalentSales
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['amount', 'account'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'amount': row.get('amount'), 'account_id': row.get('account'),
                  'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")

0
import os
from settings import MEDIA_ROOT

@login_required
def delete_attachment(request):
    if request.POST['type'] == 'sales':
        obj = get_object_or_404(SalesAttachment, day_journal__company=request.user.currently_activated_company, id=request.POST['id'])
        path = os.path.join(MEDIA_ROOT, str(obj.attachment))
        os.remove(path)
        obj.delete()
    elif request.POST['type'] == 'purchase':
        obj = get_object_or_404(PurchaseAttachment, day_journal__company=request.user.currently_activated_company, id=request.POST['id'])
        path = os.path.join(MEDIA_ROOT, str(obj.attachment))
        os.remove(path)
        obj.delete()
    elif request.POST['type'] == 'other':
        obj = get_object_or_404(OtherAttachment, day_journal__company=request.user.currently_activated_company, id=request.POST['id'])
        path = os.path.join(MEDIA_ROOT, str(obj.attachment))
        os.remove(path)
        obj.delete()
    elif request.POST['type'] == 'bank':
        obj = get_object_or_404(BankAttachment, day_journal__company=request.user.currently_activated_company, id=request.POST['id'])
        path = os.path.join(MEDIA_ROOT, str(obj.attachment))
        os.remove(path)
        obj.delete()
    return HttpResponse(json.dumps({'success': True}), mimetype="application/json")


@login_required
def save_attachments(request):
    if request.POST['type'] == 'sales':
        model = SalesAttachment
    elif request.POST['type'] == 'purchase':
        model = PurchaseAttachment
    elif request.POST['type'] == 'other':
        model = OtherAttachment
    elif request.POST['type'] == 'bank':
        model = BankAttachment
    captions = request.POST.getlist('captions')
    attachments = request.FILES.getlist('attachments')
    day_journal, created = DayJournal.objects.get_or_create(date=request.POST['day'],
                                                            company=request.user.currently_activated_company, defaults={'cheque_deposit': 0,
                                                                                               'cash_deposit': 0,
                                                                                               'cash_withdrawal': 0,
                                                                                               'cash_actual': 0})
    lst = []
    for i, attachment in enumerate(attachments):
        attached = model(attachment=attachment, description=captions[i], day_journal=day_journal)
        attached.save()
        lst.append(
            {'name': attachment.name, 'caption': captions[i], 'id': attached.id, 'link': attached.attachment.url})
    return HttpResponse(json.dumps(lst), mimetype="application/json")


@login_required
def save_lotto_sales_as_per_dispenser(request):
    params = json.loads(request.body)
    journal = get_journal(request)
    if type(journal) == dict:
        return HttpResponse(json.dumps({'error_message': journal['error']}), mimetype="application/json")
    if params.get('lotto_sales_dispenser_amount'):
        journal.lotto_sales_dispenser_amount = params.get('lotto_sales_dispenser_amount')
    if params.get('lotto_sales_register_amount'):
        journal.lotto_sales_register_amount = params.get('lotto_sales_register_amount')
    if params.get('scratch_off_sales_register_amount'):
        journal.scratch_off_sales_register_amount = params.get('scratch_off_sales_register_amount')
    journal.status = 'Unapproved'
    journal.save()
    return HttpResponse(json.dumps({'id': journal.id}), mimetype="application/json")


@login_required
def save_sales_register(request):
    params = json.loads(request.body)
    journal = get_journal(request)
    if type(journal) == dict:
        return HttpResponse(json.dumps({'error_message': journal['error']}), mimetype="application/json")
    if params.get('register_sales_amount'):
        journal.register_sales_amount = params.get('register_sales_amount')
    if params.get('register_sales_tax'):
        journal.register_sales_tax = params.get('register_sales_tax')
    journal.status = 'Unapproved'
    journal.save()
    return HttpResponse(json.dumps({'id': journal.id}), mimetype="application/json")


@login_required
def save_vendor_payout(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = VendorPayout
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['vendor', 'amount', 'paid', 'type'])
        if row.get('type') == 'new':
            if not invalid_attrs:
                invalid_attrs = []
            if invalid(row, ['purchase_ledger']):
                invalid_attrs.append(invalid(row, ['purchase_ledger'])[0])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue

        values = {'sn': index + 1, 'vendor_id': row.get('vendor'), 'amount': row.get('amount'),
                  'purchase_ledger_id': row.get('purchase_ledger'),
                  'paid_id': row.get('paid'), 'type': row.get('type'), 'remarks': row.get('remarks'),
                  'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_vendor_charge(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = VendorCharge
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['vendor', 'amount'])
        if row.get('type') == 'new':
            if not invalid_attrs:
                invalid_attrs = []
            if invalid(row, ['purchase_ledger']):
                invalid_attrs.append(invalid(row, ['purchase_ledger'])[0])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue

        values = {'sn': index + 1, 'vendor_id': row.get('vendor'), 'amount': row.get('amount'),
                  'purchase_ledger_id': row.get('purchase_ledger'), 'remarks': row.get('remarks'),
                  'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_deposits(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = Deposits
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['deposit_in', 'deposit_from', 'amount'])
        if row.get('type') == 'new':
            if not invalid_attrs:
                invalid_attrs = []
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue

        deposit_in = Account.objects.filter(id=row.get('deposit_in'))
        deposit_from = Account.objects.filter(id=row.get('deposit_from'))

        values = {'sn': index + 1, 'deposit_in': deposit_in[0], 'amount': row.get('amount'),
                  'deposit_from': deposit_from[0], 'remarks': row.get('remarks'),
                  'day_journal': day_journal}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def save_other_payout(request):
    params = json.loads(request.body)
    dct = {'invalid_attributes': {}, 'saved': {}}
    model = OtherPayout
    day_journal = get_journal(request)
    if type(day_journal) == dict:
        return HttpResponse(json.dumps({'error_message': day_journal['error']}), mimetype="application/json")
    for index, row in enumerate(params.get('rows')):
        invalid_attrs = invalid(row, ['paid_to', 'amount', 'paid'])
        if invalid_attrs:
            dct['invalid_attributes'][index] = invalid_attrs
            continue
        values = {'sn': index + 1, 'paid_to_id': row.get('paid_to'), 'amount': row.get('amount'),
                  'paid_id': row.get('paid'), 'day_journal': day_journal, 'remarks': row.get('remarks')}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['saved'][index] = submodel.id
    delete_rows(params.get('deleted_rows'), model)
    day_journal.status = 'Unapproved'
    day_journal.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@login_required
def last_lotto_detail(request, journal_date):
    try:
        # last_journal = DayJournal.objects.filter(date=journal_date, lotto_detail__isnull=False,
        # company=request.user.currently_activated_company).order_by('date')[0]

        tot = []
        data = ScratchOffLatest.objects.filter(company=request.user.currently_activated_company, date=journal_date).order_by('id')
        for item in data:
            temp = []
            for item2 in item.rows.all():
                temp.append(model_to_dict(item2))
            tot.append(temp)
        addn = []
        try:
            rang = max(map(lambda x: len(x), tot))
        except ValueError:
            rang = 0
        in_count = []
        out_count = []
        rate = []
        pck_count = []
        for i in range(rang):
            in_c = None
            out_c = None
            pck = None
            rat = None
            temp_add = 0
            for j in range(len(tot)):
                try:
                    addition = tot[j][i].get('addition', 0)
                    in_c = tot[j][i].get('in_count', 0) if in_c is None else in_c
                    out_c = tot[j][i].get('out_count', 0)
                    pck = tot[j][i].get('packet_count', 0)
                    rat = tot[j][i].get('rate', 0)
                except IndexError:
                    addition = 0
                if addition is None:
                    addition = 0
                temp_add += addition
            in_count.append(in_c)
            out_count.append(out_c)
            addn.append(temp_add)
            rate.append(rat)
            pck_count.append(pck)
        final = []
        for i in range(rang):
            temp = {}
            temp['id'] = i + 1
            temp['sn'] = i + 1
            temp['rate'] = rate[i]
            temp['pack_count'] = pck_count[i]
            temp['day_open'] = in_count[i]
            temp['day_close'] = out_count[i]
            temp['addition'] = addn[i]
            final.append(temp)
        # print "lott", last_journal.lotto_detail.all(), "new ", final
        # lotto_detail = last_journal.lotto_detail.all()

        # lst = LottoDetailSerializer(lotto_detail).data
        # print final
        return HttpResponse(json.dumps(final), mimetype="application/json")
    except IndexError:
        return HttpResponse(json.dumps([]), mimetype="application/json")


@group_required('SuperOwner', 'Owner', 'Supervisor')
def approve(request):
    params = json.loads(request.body)
    dct = {}
    try:
        journal = DayJournal.objects.get(date=params.get('date'), company=request.user.currently_activated_company)
    except DayJournal.DoesNotExist:
        dct['error_message'] = 'Day Journal needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    status = journal.backend_approve()
    dct['redirect_to'] = '/day/' + str(params.get('date'))
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('SuperOwner', 'Owner', 'Supervisor')
def unapprove(request, journal_date):
    obj = DayJournal.objects.get(company=request.user.currently_activated_company, date=journal_date)
    status = obj.backend_unapprove()
    return redirect('/day/' + str(journal_date))


def makelist(value, n):
    if type(value) != list:
        return value
    else:
        lis = []
        for i, v in enumerate(n):
            if i == 0:
                a = 0
            else:
                a = sum(n[:i])

            chunks = value[a:sum(n[:i + 1])]
            lis.append(chunks)
        return lis


def find_li(value):
    lis = []
    for i in range(12, 0, -1):
        lis.append(0)
    if len(value) == 0:
        return [1]
    check = value[0][0].month
    count = 0
    for item in value:
        if check == item[0].month:
            count += 1
        else:
            lis[check - 1] = count
            count = 1
            check = item[0].month

        if item == value[len(value) - 1]:
            lis[check - 1] = count
    return lis


# #### SCRATCH OFF LATEST:
from dayjournal.models import ScratchOffLatest, ScratchOffLatestRow
from dayjournal.forms import ScratchOffLatestForm
from dayjournal.serializers import ScratchOffLatestSerializer
import datetime

from django.forms.models import model_to_dict

@login_required
def scratch_off_latest(request, id=None):
    if id:
        scratch_off = get_object_or_404(ScratchOffLatest, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
        scratch_off.date = scratch_off.date.strftime("%m/%d/%Y")
    else:
        exixting_scratch_off_latests = ScratchOffLatest.objects.filter(company=request.user.currently_activated_company,
                                                                   date=date.today(),
                                                                   user=request.user)
        if len(exixting_scratch_off_latests) > 0:
            id = exixting_scratch_off_latests[:1][0].id
            scratch_off = get_object_or_404(ScratchOffLatest, id=id, company=request.user.currently_activated_company)
            scenario = 'Update'
            scratch_off.date = scratch_off.date.strftime("%m/%d/%Y")
        else:
            scratch_off = ScratchOffLatest(date=date.today().strftime('%m/%d/%Y'), company=request.user.currently_activated_company)
            scenario = 'New'

    form = ScratchOffLatestForm(instance=scratch_off, company=request.user.currently_activated_company)
    scratch_off_data = ScratchOffLatestSerializer(scratch_off).data

    if type(scratch_off_data['date']) == datetime.date:
        dates = scratch_off_data['date']
        scratch_off_data['date'] = dates.strftime("%m/%d/%Y")
    return render(request, 'scratch_off_latest.html', {'form': form, 'scenario': scenario, 'data': scratch_off_data})


@login_required
def save_scratch_off_latest(request, id=None):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        scratch_off = ScratchOffLatest.objects.get(id=params.get('id'), company=request.user.currently_activated_company)
    else:
        if id:
            scratch_off = ScratchOffLatest.objects.get(id=params.get('id'), company=request.user.currently_activated_company)
        else:
            scratch_off = ScratchOffLatest(company=request.user.currently_activated_company)

    scratch_off_values = {'in_time': params.get('in_time'),'out_time': params.get('out_time'),
                   'date': date(int(params.get('date').split('/')[2]), int(params.get('date').split('/')[0]),int(params.get('date').split('/')[1])),\
                   'scratch_off_id': params.get('scratch_off'), 'company': request.user.currently_activated_company, 'user': request.user}
    scratch_off = save_model(scratch_off, scratch_off_values)
    dct['id'] = scratch_off.id
    model = ScratchOffLatestRow
    for index, row in enumerate(params['particulars']['rows']):
        if invalid(row, ['rate', 'packet_count', 'in_count', 'out_count']):
            continue

        values = {'sn': index + 1, 'rate': row.get('rate'), 'packet_count': row.get('packet_count'),
                  'in_count': row.get('in_count'), 'out_count': row.get('out_count'),
                  'scratch_off': scratch_off, 'addition': row.get('addition') or '0.00' }
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
    delete_rows(params.get('particulars').get('deleted_rows'), model)
    dct['redirect_to'] = '/day/scratch-off-latest/' + str(dct['id'])

    return HttpResponse(json.dumps(dct), mimetype='application/json')


@login_required
def get_previous_scratch(request, date=datetime.date.today().strftime("%Y-%m-%d"), id=None):
    date_object = datetime.datetime.strptime(date, "%Y-%m-%d")
    if not id:
        scratch = ScratchOffLatest.objects.filter(company=request.user.currently_activated_company, date = date_object, user= request.user)
    else:
        scratch = ScratchOffLatest.objects.filter(company=request.user.currently_activated_company, date = date_object, id=id)
    if not scratch:
        datas = []
        scratch  = ScratchOffLatest.objects.filter(company=request.user.currently_activated_company, date = date_object)
        if len(scratch) > 0:
            for item in scratch[len(scratch)-1].rows.all():
                temp = {}
                dat = model_to_dict(item)
                temp['in_count'] = dat['out_count']
                temp['packet_count'] = dat['packet_count']
                temp['rate'] = dat['rate']
                temp['sn'] = dat['sn']
                temp['out_count'] = 0
                temp['addition'] = 0
                temp['id'] = None
                datas.append(temp)

        scratch_off_data = dict()
        scratch_off_data['rows'] = datas
        scratch_off_data['id'] = None
        scratch_off_data['date'] = date_object.strftime("%m/%d/%Y")
        scratch_off_data['int_time'] = ""
        scratch_off_data['out_time'] = ""
        scratch_off_data['company'] = request.user.currently_activated_company.id
        scratch_off_data['user'] = None
    else:
        datas = []
        if len(scratch) > 0:
            for item in scratch[len(scratch)-1].rows.all():
                dat = model_to_dict(item)
                datas.append(dat)
        scratch_off_data = dict()
        scratch_off_data['rows'] = datas
        scratch_off_data['id'] = None
        scratch_off_data['date'] = date_object.strftime("%m/%d/%Y")
        scratch_off_data['int_time'] = ""
        scratch_off_data['out_time'] = ""
        scratch_off_data['company'] = request.user.currently_activated_company.id
        scratch_off_data['user'] = None

    return HttpResponse(json.dumps(scratch_off_data), mimetype="application/json")



@login_required
def list_scratch_off_latest(request):
    if request.method == "POST":
        search_text = request.POST.get('search-text')
        result = watson.search(search_text,models=(ScratchOffLatest.objects.filter(company=request.user.currently_activated_company),))
        result_obj = [res.object for res in result]
        res = []
        for item in result_obj:
            if type(item) == ScratchOffLatest:
                res.append(item)
        res = list(set(res))
        return render(request, 'list_scratch_off_latest.html', {'scratch_off_items': res})
    if request.method == "GET":
        dat = request.GET.get('date')
        if dat is not None:
            scratch_off_items = ScratchOffLatest.objects.filter(company = request.user.currently_activated_company, date = dat)
            return render(request,'list_scratch_off_latest.html',{'scratch_off_items':scratch_off_items})
        else:
            scratch_off_items = ScratchOffLatest.objects.filter(company = request.user.currently_activated_company).order_by('-date')
            return render(request,'list_scratch_off_latest.html',{'scratch_off_items':scratch_off_items})

@login_required
def search_scratch_off_latest(request):
    if request.is_ajax():
        text = request.POST['text']
        result = watson.search(text,models=(ScratchOffLatest.objects.filter(company=request.user.currently_activated_company) , ))
        datas = []
        for item in result:
            if item.object is not None:
                temp = {}
                if type(item.object) == ScratchOffLatest:
                    temp['title'] = item.object.user.username
                    temp['url'] = item.object.get_absolute_url()
                    datas.append(temp)
        return HttpResponse(json.dumps(datas), mimetype="application/json")


@login_required
def cash_short_excess_report(request, year=None):
    year_list = DayJournal.objects.filter(company=request.user.currently_activated_company).values_list('date', flat=True)
    year_list = sorted(list(set([x.year for x in year_list])))[::-1]
    obj = []
    if year is None:
        year = date.today().year
    for month in range(12):
        try:
            item = DayJournal.objects.filter(date__year=year, date__month=month+1, company=request.user.currently_activated_company).order_by('-date')
        except DayJournal.DoesNotExist:
            item = None
        obj.append(item)
    return render(request, 'cash-short-excess-report.html', {'obj': obj, 'year_list': year_list})
