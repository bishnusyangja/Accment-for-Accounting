__author__ = 'bishnu'


from django import forms
from functools import partial
from datetime import date
# from django.forms.util import ErrorDict
DateInput = partial(forms.DateInput, {'class': 'dateinput'})


def add_zero(num):
    if len(num) == 1:
        return '0' + str(num)
    else:
        return num


def format_date(value):
    # return value
    return add_zero(str(value.month)) + '/' + add_zero(str(value.day)) + '/' + str(value.year)


class DateRangeForm(forms.Form):
    first = format_date(date(date.today().year, 1, 1))
    last = format_date(date.today())

    start_date = forms.DateField(widget=DateInput(), initial=first)
    end_date = forms.DateField(widget=DateInput(), initial=last)
  
    def clean(self):
        if self.cleaned_data.get('start_date') > self.cleaned_data.get('end_date'):
            raise forms.ValidationError('Start date must be less than end date')
        if self.cleaned_data.get('start_date') > date.today() or self.cleaned_data.get('end_date') > date.today():
            raise forms.ValidationError('Date can not be greater than today')
        return self.cleaned_data


class BalanceSheetDateRangeForm(forms.Form):
    end_date = forms.DateField(widget=DateInput(),initial=format_date(date.today()))

    def clean(self):
        if self.cleaned_data.get('end_date') > date.today():
            raise forms.ValidationError('Date can not be greater than today')
        return self.cleaned_data


