import django_filters

from ledger.models import Category, Account, JournalEntry
import filter_extra

#IN LISTING PAGE OF ALL LEDGERS
class LedgerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_type='icontains')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(LedgerFilter, self).__init__(*args, **kwargs)
        self.filters['category'].field.queryset = Category.objects.filter(company=company)


    class Meta:
        model = Account
        fields = ['name', 'category']


#IN EACH ACCOUNT OF A LEDGER
class LedgerAccountFilter(django_filters.FilterSet):
    date = filter_extra.DateRangeFilter(label='Date Range')
    # content_type = django_filters.CharFilter(lookup_type='icontains')


    def __init__(self, *args, **kwargs):
        super(LedgerAccountFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = JournalEntry
        fields = ['date']

