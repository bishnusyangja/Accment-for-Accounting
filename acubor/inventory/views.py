import json
from datetime import date

from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from users.models import group_required
from models import Item, InventoryAccount, Category, Unit, PhysicalStockVoucher, PhysicalStockRow, InventoryLedger
from serializers import ItemSerializer, InventoryAccountSerializer, InventoryCategorySerializer, \
    PhysicalStockVoucherSerializer
from forms import ItemForm, CategoryForm, UnitForm, PhysicalStockForm
from inventory.filters import InventoryItemFilter
from lib import invalid, save_model, all_empty_in_dict
from django.core.context_processors import csrf
from inventory.templatetags.filters import handler
from filters import PhysicalStockVoucherFilter
from ledger.models import delete_rows
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


def empty_to_None(dict, list_of_attr):
    for attr in list_of_attr:
        if dict.get(attr) == '':
            dict[attr] = None
    return dict


@login_required
def accounts_as_json(request):
    accounts = InventoryAccount.objects.filter(company=request.user.currently_activated_company)
    items_data = InventoryAccountSerializer(accounts).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


@login_required
def accounts_by_day_as_json(request, day):
    accounts = InventoryAccount.objects.filter(company=request.user.currently_activated_company)
    items_data = InventoryAccountSerializer(accounts, day=day).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


@login_required
def items_by_day_as_json(request, day):
    items = Item.objects.filter(company=request.user.currently_activated_company)
    items_data = ItemSerializer(items, day=day).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


@login_required
def item_form(request, id=None):
    if id:
        item = get_object_or_404(Item, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
    else:
        item = Item()
        scenario = 'Create'

    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    message = None
    if request.POST:
        form = ItemForm(data=request.POST, instance=item, company=request.user.currently_activated_company)
        if form.is_valid():
            item = form.save(commit=False)
            item.company = request.user.currently_activated_company
            name_list = Item.objects.filter(name=item.name, company=request.user.currently_activated_company)
            if name_list and scenario == "Create":
                msg = 'Duplicate Item name is not allowed.'
                return render(request, 'item_form.html', {
                        'scenario': scenario,
                        'form': form,
                        'msg': msg,
                        'base_template': base_template,
                    })
            item.save()

            message = "Saved!"
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': ItemSerializer(item).data})
            return render(request, 'item_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
        'message': message,

    })
    else:
        form = ItemForm(instance=item, company=request.user.currently_activated_company)
    return render(request, 'item_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,

    })


@login_required
def view_stock_ledger(request, id):
    try:
        item = Item.objects.get(id=id)
        inventory_account = item.account
        inventory_entries = InventoryLedger.objects.filter(account=inventory_account, company=request.user.currently_activated_company,
                                                           date__lte=date.today())
        base_template = 'dashboard.html'
        return render(request, 'view_stock_ledger.html',
                      {'inventory_account': inventory_account, 'inventory_entries': inventory_entries,
                       'base_template': base_template})
    except ObjectDoesNotExist:
        raise Http404


@login_required
def create_item(request, id=None):
    """
    @param request:
    @return: JSON for account for added Inventory Item
    """
    if id:
        try:
            inv_cat = Category.objects.filter(id=id, company=request.user.currently_activated_company)
        except Category.DoesNotExist:
            inv_cat = None
    else:
        inv_cat = None

    item = Item()
    if inv_cat is not None:
        item.category = inv_cat[0]
    scenario = 'Create'
    for query in request.GET:
        setattr(item, query, request.GET[query])

    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'

    if request.POST:
        form = ItemForm(data=request.POST, instance=item, company=request.user.currently_activated_company)
        if form.is_valid():
            name_list = Item.objects.filter(name=form.data['name'], company=request.user.currently_activated_company)
            if name_list and scenario == "Create":
                msg = 'Duplicate Item name is not allowed.'
                return render(request, 'item_form.html', {
                        'scenario': scenario,
                        'form': form,
                        'msg': msg,
                        'base_template': base_template,
                    })
            item = form.save(commit=False)
            item.company = request.user.currently_activated_company
            item.save()
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': ItemSerializer(item).data})
            return redirect('/inventory/items/')
    else:
        form = ItemForm(instance=item, company=request.user.currently_activated_company)
        form.hide_field(request)

    return render(request, 'item_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })


@login_required
def delete_inventory_item(request, id):
    obj = get_object_or_404(Item, id=id, company=request.user.currently_activated_company)
    obj.delete()
    return redirect('/inventory/items/')


@login_required
def items_as_json(request):
    items = Item.objects.filter(company=request.user.currently_activated_company)
    items_data = ItemSerializer(items).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


@login_required
def list_all_items(request):
    objects = Item.objects.filter(company=request.user.currently_activated_company)
    filtered_items = InventoryItemFilter(request.GET, queryset=objects, company=request.user.currently_activated_company)
    return render(request, 'list_all_items.html', {'objects': filtered_items})


@login_required
def list_categories(request):
    categories = Category.objects.filter(company=request.user.currently_activated_company)
    return render(request, 'list_inventory_categories.html', {'categories': categories})


@login_required
def create_category(request):
    category = Category()
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'

    message = None
    if request.POST:
        form = CategoryForm(data=request.POST, company=request.user.currently_activated_company)
        if form.is_valid():
            category = form.save(commit=False)
            category.company = request.user.currently_activated_company
            name_list = Category.objects.filter(name=category.name, company=request.user.currently_activated_company)
            if name_list :
                msg = 'Duplicate Category name is not allowed.'
                return render(request, 'inventory_category_create_form.html', {
                        'form': form,
                        'msg': msg,
                        'base_template': base_template,
                    })
            category.save()
            message = "Saved!"
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': InventoryCategorySerializer(category).data})
            return render(request, 'inventory_category_create_form.html', {
                        'form': form,
                        'message': message,
                        'base_template': base_template,
                    })
    else:
        form = CategoryForm(instance=category, company=request.user.currently_activated_company)

    return render(request, 'inventory_category_create_form.html', {
        'form': form,
        'base_template': base_template,
    })


@login_required
def update_category(request, id):
    if id:
        category = get_object_or_404(Category, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
    else:
        category = Category()
        scenario = 'Create'
    # category = get_object_or_404(Category, id=id, company=request.user.currently_activated_company)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    message = None
    if request.POST:
        form = CategoryForm(data=request.POST, instance=category, company=request.user.currently_activated_company)
        if form.is_valid():
            category = form.save(commit=False)
            category.company = request.user.currently_activated_company
            name_list = Category.objects.filter(name=category.name, company=request.user.currently_activated_company)
            if name_list and scenario=="Create":
                msg = 'Duplicate Category name is not allowed.'
                return render(request, 'inventory_category_update_form.html', {
                        'form': form,
                        'msg': msg,
                        'base_template': base_template,
                    })
            category.save()
            message = "Saved!"
            return render(request, 'inventory_category_update_form.html', {
        'form': form,
        'base_template': base_template,
        'message' : message
    })
    else:
        form = CategoryForm(instance=category, company=request.user.currently_activated_company)

    return render(request, 'inventory_category_update_form.html', {
        'form': form,
        'base_template': base_template,
        'message' : message
    })


@login_required
def delete_category(request, id):
    category = get_object_or_404(Category, id=id, company=request.user.currently_activated_company)
    category.delete()
    return redirect('/inventory/categories/')


@login_required
def unit_form(request, id=None):
    if id:
        obj = get_object_or_404(Unit, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
    else:
        obj = Unit(company=request.user.currently_activated_company)
        scenario = 'Create'
    message = None
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    if request.POST:
        form = UnitForm(data=request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.company = request.user.currently_activated_company
            name_list = Unit.objects.filter(name=obj.name, company=request.user.currently_activated_company)
            print name_list, scenario
            if name_list and scenario == "Create":
                msg = 'Duplicate Unit name is not allowed.'
                print msg
                return render(request, 'unit_form.html', {
                        'scenario': scenario,
                        'form': form,
                        'msg': msg,
                        'base_template': base_template,
                    })
            obj.save()
            message = "Saved!"
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': {'name': obj.name, 'id': obj.id}})
            return render(request, 'unit_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
        'message' : message
    })
    else:
        form = UnitForm(instance=obj)

    return render(request, 'unit_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
        'message': message
    })


@login_required
def list_units(request):
    objs = Unit.objects.filter(company=request.user.currently_activated_company)
    return render(request, 'list_units.html', {'objects': objs})


@login_required
def delete_unit(request, id):
    obj = get_object_or_404(Unit, id=id, company=request.user.currently_activated_company)
    obj.delete()
    return redirect(reverse_lazy('list_units'))


@login_required
def physical_stock(request, id=None):
    approved = 0
    from core.models import VoucherSetting
    from core.models import CompanySetting

    try:
        voucher_setting = VoucherSetting.objects.get(company=request.user.currently_activated_company)
        company_setting = CompanySetting.objects.get(company=request.user.currently_activated_company)
    except CompanySetting.DoesNotExist:
        # TODO Add a flash message
        return redirect('/settings/company')

    if id:
        physical_stock_voucher = get_object_or_404(PhysicalStockVoucher, id=id, company=request.user.currently_activated_company)
        physical_stock_voucher.date = physical_stock_voucher.date.strftime("%m/%d/%Y")
        scenario = 'Update'
    else:
        physical_stock_voucher = PhysicalStockVoucher(date=date.today().strftime("%m/%d/%Y"),
                                                      company=request.user.currently_activated_company
        )
        scenario = 'Create'
    form = PhysicalStockForm(data=request.POST, instance=physical_stock_voucher, company=request.user.currently_activated_company)
    physical_stock_data = PhysicalStockVoucherSerializer(physical_stock_voucher).data

    physical_stock_data['read_only'] = {
        'physical_stock_prefix': voucher_setting.physicalstock_prefix,
        'physical_stock_suffix': voucher_setting.physicalstock_suffix,
    }
    filtered_items = []
    if physical_stock_voucher.status == 'Approved':
        approved = 1
        items = PhysicalStockVoucher.objects.filter(company=request.user.currently_activated_company, id=id)
        filtered_items = PhysicalStockVoucherFilter(request.GET, queryset=items, company=request.user.currently_activated_company)

    return render(request, 'physical_stock_form.html', {'objects': filtered_items, 'form': form, 'approved': approved,
                                                        'data': physical_stock_data, 'scenario': scenario})


@login_required
def save_physical_stock(request):
    params = json.loads(request.body)
    dct = {'rows': {}}

    vch_no = params.get('voucher_no')
    try:
        vch_no = int(vch_no)
    except ValueError:
        dct['error_message'] = 'Only numbers are allowed in voucher no.'
        return HttpResponse(json.dumps(dct), mimetype='application/json')

    if params.get('id'):
        physical_stock = PhysicalStockVoucher.objects.get(id=params.get('id'))
    else:
        physical_stock = PhysicalStockVoucher(company=request.user.currently_activated_company)
        # if not created:
    try:
        existing = PhysicalStockVoucher.objects.get(voucher_no=params.get('voucher_no'), company=request.user.currently_activated_company)
        if physical_stock.id is not existing.id:
            return HttpResponse(json.dumps({'error_message': 'Physical Stock Voucher No. already exists'}),
                                mimetype="application/json")
    except PhysicalStockVoucher.DoesNotExist:
        pass
    physical_stock_values = {'voucher_no': params.get('voucher_no'),
                             'description': params.get('description'),
                             'date': params.get('date'),
                             'company': request.user.currently_activated_company,
                             'status': 'Unapproved',
                             'total_amount': params.get('total')
    }
    dates = physical_stock_values['date'].encode("utf-8").split("/")
    physical_stock_values['date'] = dates[2] + '-' + dates[0] + '-' + dates[1]

    total_amount = 0
    for row in params.get('particulars').get('rows'):
        total_amount += float(row.get('amount'))
    physical_stock_values['total_amount'] = total_amount

    physical_stock = save_model(physical_stock, physical_stock_values)
    dct['id'] = physical_stock.id
    model = PhysicalStockRow
    for index, row in enumerate(params.get('particulars').get('rows')):
        if invalid(row, ['item_id', 'rate', 'quantity']):
            continue
        values = {'sn': index + 1, 'item_id': row.get('item_id'),
                  'rate': row.get('rate'), 'quantity': row.get('quantity'),
                  'amount': row.get('amount'), 'physical_stock_voucher': physical_stock}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)

        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('particulars').get('deleted_rows'), model)
    if params.get('continue'):
        dct = {'redirect_to': str(reverse_lazy('new_physical_stock'))}
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Owner', 'SuperOwner', 'Supervisor')
def approve_physical_stock(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        voucher = PhysicalStockVoucher.objects.get(id=params.get('id'))
        status = voucher.backend_approve()
        if status == 'Unapproved':
            dct['error_message'] = 'An error occured while approving the voucher.'
    else:
        dct['error_message'] = 'Voucher needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    dct['redirect_to'] = '/inventory/physicalstock/' + str(params.get('id'))
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Owner', 'SuperOwner', 'Supervisor')
def unapprove_physical_stock(request, id):
    if id:
        obj = PhysicalStockVoucher.objects.get(company=request.user.currently_activated_company, id=id)
        obj.backend_unapprove()
    return redirect('/inventory/physicalstock/' + str(id))


@login_required
def cancel_physical_stock(request):
    r = save_physical_stock(request)
    dct = json.loads(r.content)
    if dct.get('id'):
        obj = PhysicalStockVoucher.objects.get(id=dct.get('id'))
        obj.backend_unapprove()
        obj.status = 'Cancelled'
    obj.save()
    return r


@login_required
def delete_physical_stock(request, voucher_no):
    obj = PhysicalStockVoucher.objects.get(voucher_no=voucher_no, company=request.user.currently_activated_company)
    if obj:
        obj.backend_unapprove()
        obj.delete()
    return redirect(reverse('all_physical_stocks'))


@login_required
def all_physical_stocks(request):
    items = PhysicalStockVoucher.objects.filter(company=request.user.currently_activated_company)
    filtered_items = PhysicalStockVoucherFilter(request.GET, queryset=items, company=request.user.currently_activated_company)
    return render(request, 'list_physical_stock.html', {'objects': filtered_items})


