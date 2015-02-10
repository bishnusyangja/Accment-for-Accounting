import datetime
import operator

from django import forms
from django_filters import Filter
from django.db.models import Q
from django_filters import CharFilter


class MultiFieldFilter(CharFilter):
    """
    This filter preforms an OR query on the defined fields from a
    single entered value.

    The following will work similar to the default UserAdmin search::

        class UserFilterSet(FilterSet):
            search = MultiFieldFilter(['username', 'first_name',
                                       'last_name', 'email'])
            class Meta:
                model = User
                fields = ['search']
    """

    def __init__(self, fields, *args, **kwargs):
        super(MultiFieldFilter, self).__init__(*args, **kwargs)
        self.fields = fields
        self.lookup_type = 'icontains'
        self.lookup_types = [
            ('^', 'istartswith'),
            ('=', 'iexact'),
            ('@', 'search'),
        ]

    def filter(self, qs, value):
        if not self.fields or not value:
            return qs

        lookups = [self._get_lookup(str(field)) for field in self.fields]
        queries = [Q(**{lookup: value}) for lookup in lookups]
        qs = qs.filter(reduce(operator.or_, queries))
        return qs

    def _get_lookup(self, field_name):
        for key, lookup_type in self.lookup_types:
            if field_name.startswith(key):
                return "%s__%s" % (field_name[len(key):], lookup_type)
        return "%s__%s" % (field_name, self.lookup_type)


class DateRangeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        attrs_from = {'class': 'date-picker'}
        attrs_to = {'class': 'date-picker'}

        if attrs:
            attrs_from.update(attrs)
            attrs_to.update(attrs)

        widgets = (forms.TextInput(attrs=attrs_from), forms.TextInput(attrs=attrs_to))
        super(DateRangeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]

    def format_output(self, rendered_widgets):
        return '<div class="date-range">' + ' - '.join(rendered_widgets) + '</div>'


class DateRangeField(forms.MultiValueField):
    widget = DateRangeWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.DateField(),
            forms.DateField(),
        )
        super(DateRangeField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return slice(*data_list)
        return None


class DateRangeFilter(Filter):
    field_class = DateRangeField

    def filter(self, qs, value):
        date_start = datetime.datetime.combine(value.start, datetime.time(0, 0, 0))
        date_stop = datetime.datetime.combine(value.stop, datetime.time(23, 59, 59))

        if value:
            lookup = '%s__range' % self.name
            return qs.filter(**{lookup: (date_start, date_stop)})
        return qs

