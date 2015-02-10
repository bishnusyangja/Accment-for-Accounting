import django_filters

import filter_extra
from inventory.models import InventoryAccount, Item
from dayjournal.models import DayJournal


class InventoryItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(InventoryItemFilter, self).__init__(*args, **kwargs)


    class Meta:
        model = Item
        fields = ['name', 'category']


class InventoryAccountFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(InventoryAccount, self).__init__(*args, **kwargs)

    class Meta:
        model = InventoryAccount


class DayjournalFilter(django_filters.FilterSet):
    date = filter_extra.DateRangeFilter(label='Date Range')
    # content_type = django_filters.CharFilter(lookup_type='icontains')
    def __init__(self, *args, **kwargs):
        super(DayjournalFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = DayJournal
        fields = ['date']
