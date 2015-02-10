from datetime import date, datetime

from django.shortcuts import render

from mptt.templatetags.mptt_tags import cache_tree_children
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from forms import DateRangeForm, BalanceSheetDateRangeForm

from ledger.models import Category
from lib import zero_for_none
from inventory.models import PhysicalStockVoucher


# cost of goods sold view

def get_cogs_dict(company, start, end):
    opening_stock = PhysicalStockVoucher.objects.filter(company=company, date=start)
    closing_stock = PhysicalStockVoucher.objects.filter(company=company, date=end)

    if opening_stock:
        opening_stock_amount = 0.0
        for each in opening_stock:
            if each.status == "Approved":
                opening_stock_amount = opening_stock_amount + zero_for_none(each.get_total_amount())
    else:
        opening_stock_amount = 0.0

    if closing_stock:
        closing_stock_amount = 0.0
        for each in closing_stock:
            if each.status == "Approved":
                closing_stock_amount = closing_stock_amount + zero_for_none(each.get_total_amount())
    else:
        closing_stock_amount = 0.0

    return {'opening_stock_amount': opening_stock_amount, 'closing_stock_amount': closing_stock_amount}


def recursive_node_to_pl_dict(node, start, end):
    result = {
        'id': node.pk,
        'name': node.name,
    }
    children = [recursive_node_to_pl_dict(c, start, end) for c in node.get_children()]

    """
    mpttModel.get_children()
    Returns a QuerySet containing the immediate children of this model instance, in tree order.
    """
    accounts = []

    for account in node.accounts.all():
        a = {'id': account.id, 'name': account.name, 'link': account.get_absolute_url(),
             'transaction_dr': zero_for_none(account.get_dr_amount(end)) - zero_for_none(
                 account.get_day_opening_dr(start)),
             'transaction_cr': zero_for_none(account.get_cr_amount(end)) - zero_for_none(
                 account.get_day_opening_cr(start))}
        if a['transaction_dr'] != a['transaction_cr']:
            accounts.append(a)
        if a['name'] == 'Profit/Loss':
            a['link'] = '/report/profit-and-loss/'
    result['accounts'] = accounts
    if children:
        result['children'] = children
    return result


def to_pl_dict(model, company, start, end):
    root_nodes = cache_tree_children(model.objects.filter(company=company))

    """
    from mptt.templatetags.mptt_tags import cache_tree_children
    cache_tree_children takes a list/queryset of model objects in MPTT left (depth-first) order,
    caches the children on each node, as well as the parent of each child node,
    allowing up and down traversal through the tree without the need for
    further queries. This makes it possible to have a recursively included
    template without worrying about database queries.
    Returns a list of top-level nodes. If a single tree was provided in its
    entirety, the list will of course consist of just the tree's root node.
    """

    dicts = []
    for n in root_nodes:
        dicts.append(recursive_node_to_pl_dict(n, start, end))
    return dicts


@login_required
def profit_and_loss(request, end_date1, count=1):
    if end_date1:
        start, end = date(date.today().year, 1, 1), datetime.strptime(end_date1, '%m-%d-%Y').date()
    else :
        start, end = date(date.today().year, 1, 1), date.today()
    dict_1 = {}
    if request.method == "POST":
        f = DateRangeForm(request.POST)
        if f.is_valid():
            data = f.cleaned_data
            start = data.get('start_date')
            end = data.get('end_date')
            dict_1 = to_pl_dict(Category, request.user.currently_activated_company, start, end)
    else:
        f = DateRangeForm()
        dict_1 = to_pl_dict(Category, request.user.currently_activated_company, start, end)

    cogs_dict = get_cogs_dict(request.user.currently_activated_company, start, end)

    dict_2 = []
    purchase = {}
    direct_expenses = {}
    for (index, dict_child) in enumerate(dict_1):
        if ['Income'].__contains__(dict_child['name']):
            for each in dict_child['children']:
                if each['name'] == 'Revenue':
                    each['id'] = 1
                if each['name'] == 'Indirect Income':
                    each['id'] = 4
                dict_2.append(each)
        if ['Expenses'].__contains__(dict_child['name']):
            for each in dict_child['children']:
                if each['name'] == 'Indirect Expenses':
                    each['id'] = 5
                    dict_2.append(each)
                if each['name'] == 'Direct Expenses':
                    direct_expenses = each
                if each['name'] == 'Purchase':
                    purchase = each

    direct_income_total, direct_expense_total, indirect_income_total, indirect_expense_total, purchase_total = 0.0, 0.0, 0.0, 0.0, 0.0

    categories = Category.objects.filter(company=request.user.currently_activated_company)
    for category in categories:
        if category.name == 'Purchase':
            purchase_total = purchase_total + category.get_duration_cat_tot_dr(start,
                                                                               end) - category.get_duration_cat_tot_cr(
                start, end)
        if category.name == 'Revenue':
            direct_income_total = direct_income_total + category.get_duration_cat_tot_cr(start,
                                                                                         end) - category.get_duration_cat_tot_dr(
                start, end)
        if category.name == 'Direct Expenses':
            direct_expense_total = direct_expense_total + category.get_duration_cat_tot_dr(start,
                                                                                           end) - category.get_duration_cat_tot_cr(
                start, end)
        if category.name == 'Indirect Income':
            indirect_income_total = indirect_income_total + category.get_duration_cat_tot_cr(start,
                                                                                             end) - category.get_duration_cat_tot_dr(
                start, end)
        if category.name == 'Indirect Expenses':
            indirect_expense_total = indirect_expense_total + category.get_duration_cat_tot_dr(start,
                                                                                               end) - category.get_duration_cat_tot_cr(
                start, end)

    cogs_sub_total = cogs_dict['opening_stock_amount'] + direct_expense_total + purchase_total

    cogs_amount = cogs_sub_total - cogs_dict['closing_stock_amount']

    net_profit_amount = direct_income_total - cogs_amount

    gross_profit_amount = net_profit_amount + indirect_income_total - indirect_expense_total

    cogs_dict_total = {
    'children': [{'name': u'Opening Stock', 'id': 1000, 'amount': cogs_dict['opening_stock_amount']}, purchase,
                 direct_expenses, {'name': u'Sub Total', 'id': 1001, 'amount': cogs_sub_total},
                 {'name': u'Closing Stock', 'id': 1002, 'amount': cogs_dict['closing_stock_amount']}], 'id': 2,
    'name': u'Cost Of Goods Sold', 'amount': cogs_amount}
    dict_2.append(cogs_dict_total)

    net_profit_dict = {'id': 3, 'name': 'Gross Profit', 'amount': net_profit_amount}
    dict_2.append(net_profit_dict)

    sorted_dict_2 = sorted(dict_2, key=lambda tup: tup['id'])

    dict = {'categories': sorted_dict_2, 'start': start, 'end': end, 'total_revenue': direct_income_total,
            'gross_profit': gross_profit_amount}
    args = {}
    args.update(csrf(request))
    args['form'] = f
    args['dict'] = dict

    return render(request, 'profit_and_loss.html', args)


# balance sheet view starts

def recursive_node_to_bs_dict(company, node, start, end, gross_profit_amount, closing_stock_amount):
    result = {
        'id': node.pk,
        'name': node.name,
    }
    children = [recursive_node_to_bs_dict(company, c, start, end, gross_profit_amount, closing_stock_amount) for c in
                node.get_children()]

    """
    mpttModel.get_children()
    Returns a QuerySet containing the immediate children of this model instance, in tree order.
    """
    accounts = []

    for account in node.accounts.all():
        a = {'id': account.id, 'name': account.name}
        if zero_for_none(account.get_dr_amount(end)) != zero_for_none(account.get_cr_amount(end)):
            if Category.objects.get(company=company, name='Assets') in account.categories:
                a['amount'] = zero_for_none(account.get_dr_amount(end)) - zero_for_none(account.get_cr_amount(end))
                accounts.append(a)
            elif Category.objects.get(company=company, name='Equity') in account.categories:
                a['amount'] = zero_for_none(account.get_cr_amount(end)) - zero_for_none(account.get_dr_amount(end))
                accounts.append(a)
            elif Category.objects.get(company=company, name='Liabilities') in account.categories:
                a['amount'] = zero_for_none(account.get_cr_amount(end)) - zero_for_none(account.get_dr_amount(end))
                accounts.append(a)
        if a['name'] == 'Profit/Loss':
            a['amount'] = zero_for_none(gross_profit_amount)
            a['link'] = '/report/profit-and-loss/'
            accounts.append(a)
        if a['name'] == 'Closing Stock':
            a['amount'] = zero_for_none(closing_stock_amount)
            accounts.append(a)
    result['accounts'] = accounts
    if children:
        result['children'] = children
    return result


def to_bs_dict(model, company, start, end, gross_profit_amount, closing_stock_amount):
    root_nodes = cache_tree_children(model.objects.filter(company=company))

    """
    from mptt.templatetags.mptt_tags import cache_tree_children
    cache_tree_children takes a list/queryset of model objects in MPTT left (depth-first) order,
    caches the children on each node, as well as the parent of each child node,
    allowing up and down traversal through the tree without the need for
    further queries. This makes it possible to have a recursively included
    template without worrying about database queries.
    Returns a list of top-level nodes. If a single tree was provided in its
    entirety, the list will of course consist of just the tree's root node.
    """
    dicts = []
    for n in root_nodes:
        if n.name != 'Income' and n.name != 'Expenses' and n.name != 'Opening Balance Difference':
            dicts.append(recursive_node_to_bs_dict(company, n, start, end, gross_profit_amount, closing_stock_amount))
    return dicts


@login_required
def balance_sheet(request):
    start, end = date(date.today().year, 1, 1), date.today()
    dict_1 = []

    #P/L part
    opening_stock = PhysicalStockVoucher.objects.filter(company=request.user.currently_activated_company, date=start)
    closing_stock = PhysicalStockVoucher.objects.filter(company=request.user.currently_activated_company, date=end)

    opening_stock_amount, closing_stock_amount = 0.0, 0.0

    if opening_stock:
        for each in opening_stock:
            opening_stock_amount = opening_stock_amount + zero_for_none(each.get_total_amount())
    else:
        opening_stock_amount = 0.0

    if closing_stock:
        for each in closing_stock:
            closing_stock_amount = closing_stock_amount + zero_for_none(each.get_total_amount())
    else:
        closing_stock_amount = 0.0

    direct_income_total, direct_expense_total, indirect_income_total, indirect_expense_total, purchase_total = 0.0, 0.0, 0.0, 0.0, 0.0

    categories = Category.objects.filter(company=request.user.currently_activated_company)
    for category in categories:
        if category.name == 'Purchase':
            purchase_total = purchase_total + category.get_duration_cat_tot_dr(start,
                                                                               end) - category.get_duration_cat_tot_cr(
                start, end)
        if category.name == 'Revenue':
            direct_income_total = direct_income_total + category.get_duration_cat_tot_cr(start,
                                                                                         end) - category.get_duration_cat_tot_dr(
                start, end)
        if category.name == 'Direct Expenses':
            direct_expense_total = direct_expense_total + category.get_duration_cat_tot_dr(start,
                                                                                           end) - category.get_duration_cat_tot_cr(
                start, end)
        if category.name == 'Indirect Income':
            indirect_income_total = indirect_income_total + category.get_duration_cat_tot_cr(start,
                                                                                             end) - category.get_duration_cat_tot_dr(
                start, end)
        if category.name == 'Indirect Expenses':
            indirect_expense_total = indirect_expense_total + category.get_duration_cat_tot_dr(start,
                                                                                               end) - category.get_duration_cat_tot_cr(
                start, end)

    cogs_sub_total = opening_stock_amount + direct_expense_total + purchase_total

    cogs_amount = cogs_sub_total - closing_stock_amount

    net_profit_amount = direct_income_total - cogs_amount

    gross_profit_amount = net_profit_amount + indirect_income_total - indirect_expense_total

    #bs form check
    if request.method == "POST":
        f = BalanceSheetDateRangeForm(request.POST)
        if f.is_valid():
            data = f.cleaned_data
            end = data.get('end_date')
            dict_1 = to_bs_dict(Category, request.user.currently_activated_company, start, end, gross_profit_amount, closing_stock_amount)
    else:
        f = BalanceSheetDateRangeForm()
        dict_1 = to_bs_dict(Category, request.user.currently_activated_company, start, end, gross_profit_amount, closing_stock_amount)

    equity_cat = Category.objects.get(company=request.user.currently_activated_company, name='Equity')
    liability_cat = Category.objects.get(company=request.user.currently_activated_company, name='Liabilities')
    asset_cat = Category.objects.get(company=request.user.currently_activated_company, name='Assets')

    equity_cat_sub_tot = zero_for_none(equity_cat.get_cat_tot_cr(end)) - zero_for_none(
        equity_cat.get_cat_tot_dr(end)) + gross_profit_amount
    liability_cat_sub_tot = zero_for_none(liability_cat.get_cat_tot_cr(end)) - zero_for_none(
        liability_cat.get_cat_tot_dr(end))
    equity_and_liability_tot = equity_cat_sub_tot + liability_cat_sub_tot
    asset_cat_tot = zero_for_none(asset_cat.get_cat_tot_dr(end)) - zero_for_none(
        asset_cat.get_cat_tot_cr(end)) + closing_stock_amount

    for each in dict_1:
        if each['name'] == 'Equity':
            # dangerous code needs to be changed
            each['children'].append({'id': 999700, 'name': 'Total Equity', 'amt': equity_cat_sub_tot})
        elif each['name'] == 'Liabilities':
            each['children'].append({'id': 999800, 'name': 'Total Liabilities', 'amt': liability_cat_sub_tot})
            each['children'].append(
                {'id': 999900, 'name': 'Total Equity And Liabilities', 'amt': equity_and_liability_tot})
        elif each['name'] == 'Assets':
            each['children'].append({'id': 999990, 'name': 'Total Assets', 'amt': asset_cat_tot})

    dict_final = {'categories': dict_1, 'start': start, 'end': end}
    args = {}
    args.update(csrf(request))
    args['form'] = f
    args['dict'] = dict_final

    return render(request, 'balance_sheet.html', args)


# trial balance views starts



def recursive_node_to_dict(node, start, end):
    result = {
        'id': node.pk,
        'name': node.name,
    }
    children = [recursive_node_to_dict(c, start, end) for c in node.get_children()]

    """
    mpttModel.get_children()
    Returns a QuerySet containing the immediate children of this model instance, in tree order.
    """
    accounts = []

    for account in node.accounts.all():
        a = {'id': account.id, 'name': account.name, 'opening_dr': zero_for_none(account.get_day_opening_dr(start)),
             'opening_cr': zero_for_none(account.get_day_opening_cr(start)),
             'closing_dr': zero_for_none(account.get_dr_amount(end)),
             'closing_cr': zero_for_none(account.get_cr_amount(end)),
             'transaction_dr': zero_for_none(account.get_dr_amount(end)) - zero_for_none(
                 account.get_day_opening_dr(start)),
             'transaction_cr': zero_for_none(account.get_cr_amount(end)) - zero_for_none(
                 account.get_day_opening_cr(start))}
        if a['transaction_dr'] <> a['transaction_cr'] or a['opening_cr'] <> a['opening_dr'] or a['closing_dr'] <> a[
            'closing_cr']:
            accounts.append(a)
    result['accounts'] = accounts
    if children:
        result['children'] = children
    return result


def to_dict(model, company, start, end):
    root_nodes = cache_tree_children(model.objects.filter(company=company))

    """
    from mptt.templatetags.mptt_tags import cache_tree_children
    cache_tree_children takes a list/queryset of model objects in MPTT left (depth-first) order,
    caches the children on each node, as well as the parent of each child node,
    allowing up and down traversal through the tree without the need for
    further queries. This makes it possible to have a recursively included
    template without worrying about database queries.
    Returns a list of top-level nodes. If a single tree was provided in its
    entirety, the list will of course consist of just the tree's root node.
    """

    dicts = []
    for n in root_nodes:
        dicts.append(recursive_node_to_dict(n, start, end))
    return dicts


@login_required
def trial_balance(request):
    categories = Category.objects.filter(company=request.user.currently_activated_company)
    start, end = date(date.today().year, 1, 1), date.today()
    if request.method == "POST":
        f = DateRangeForm(request.POST)
        if f.is_valid():
            data = f.cleaned_data
            start = data.get('start_date')
            end = data.get('end_date')
    else:
        f = DateRangeForm()

    dict_1 = to_dict(Category, request.user.currently_activated_company, start, end)
    dicty = {'categories': dict_1, 'start': start, 'end': end}
    args = {}
    args.update(csrf(request))
    args['form'] = f
    args['dict'] = dicty
    args['categories'] = categories
    return render(request, 'trial_balance.html', args)





