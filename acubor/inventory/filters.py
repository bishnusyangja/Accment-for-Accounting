import django_filters
from inventory.models import InventoryAccount, Item, Category, PhysicalStockVoucher, PhysicalStockRow
import filter_extra


class PhysicalStockVoucherFilter(django_filters.FilterSet):
    voucher_no = django_filters.CharFilter(lookup_type='icontains')
    date = filter_extra.DateRangeFilter(label='Date Range')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(PhysicalStockVoucherFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = PhysicalStockVoucher
        fields = ['voucher_no', 'date']


class InventoryItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(InventoryItemFilter, self).__init__(*args, **kwargs)
        self.filters['category'].field.queryset = Category.objects.filter(company=company)

    class Meta:
        model = Item
        fields = ['name', 'category']


class InventoryAccountFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(InventoryAccount, self).__init__(*args, **kwargs)

    class Meta:
        model = InventoryAccount