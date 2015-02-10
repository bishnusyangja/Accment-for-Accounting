from datetime import date
import os
from django import forms
# from ledger.models import Transaction



class ExtFileField(forms.FileField):
    """
    Same as forms.FileField, but you can specify a file extension whitelist.

    Traceback (most recent call last):
    ...
    ValidationError: [u'Not allowed filetype!']
    """

    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        self.ext_whitelist = [i.lower() for i in ext_whitelist]

        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ExtFileField, self).clean(*args, **kwargs)
        if data is None:
            if self.required:
                raise forms.ValidationError("This file is required")
            else:
                return
        elif data is not False:
            filename = data.name
            ext = os.path.splitext(filename)[1]
            ext = ext.lower()
            if ext not in self.ext_whitelist:
                file_types = ", ".join([i for i in self.ext_whitelist])
                error = "Only allowed file types are: %s" % file_types
                raise forms.ValidationError(error)


class KOModelForm(forms.ModelForm):
    class EmailTypeInput(forms.widgets.TextInput):
        input_type = 'email'

    class NumberTypeInput(forms.widgets.TextInput):
        input_type = 'number'

    class TelephoneTypeInput(forms.widgets.TextInput):
        input_type = 'tel'

    class DateTypeInput(forms.widgets.DateInput):
        input_type = 'date'

    class DateTimeTypeInput(forms.widgets.DateTimeInput):
        input_type = 'datetime'

    class TimeTypeInput(forms.widgets.TimeInput):
        input_type = 'time'

    def __init__(self, *args, **kwargs):
        super(KOModelForm, self).__init__(*args, **kwargs)
        self.refine()

    def refine(self):
        for (name, field) in self.fields.items():
            # add HTML5 required attribute for required fields
            if field.required:
                field.widget.attrs['required'] = 'required'
            field.widget.attrs['data-bind'] = 'value: ' + name

    def hide_field(self, request):
        for query in request.GET:
            if query[-3:] == '_id':
                query = query[:-3]
            self.fields[query].widget = self.fields[query].hidden_widget()
            self.fields[query].label = ''
        return self


def invalid(row, required_fields):
    invalid_attrs = []
    for attr in required_fields:
        # if one of the required attributes isn't received or is an empty string
        if not attr in row or row.get(attr) == "":
            invalid_attrs.append(attr)
    if len(invalid_attrs) is 0:
        return False
    return invalid_attrs


def all_empty(row, required_fields):
    for attr in required_fields:
        # if one of the required attributes isn received or is not an empty string
        if attr in row and row.get(attr) != "":
            return False
    return True


def all_empty_in_dict(dct):
    for val in dct:
        if dct[val]:
            return False
    return True


def save_model(model, values):
    for key, value in values.items():
        setattr(model, key, value)
    model.save()
    return model


# def dr(account, amount):
#     if amount is None:
#         return
#     transaction = Transaction(account=account, dr_amount=amount)
#     return transaction
#
#
# def cr(account, amount, date):
#     if amount is None:
#         return
#     transaction = Transaction(account=account, cr_amount=amount)
#     return transaction


def zero_for_none(obj):
    if obj is None:
        return 0
    else:
        return obj


def none_for_zero(obj):
    if not obj:
        return None
    else:
        return obj

def add(*args):
    total = 0
    for arg in args:
        if arg == '':
            arg = 0
        total += float(arg)
    return total


def get_next_voucher_no(cls, company):
    from django.db.models import Max
    setting = company.voucher_settings
    #import pdb
    #pdb.set_trace()
    start_date = setting.voucher_number_start_date
    restart_years = setting.voucher_number_restart_years
    restart_months = setting.voucher_number_restart_months
    restart_days = setting.voucher_number_restart_days
    end_date = date(start_date.year + restart_years, start_date.month + restart_months, start_date.day + restart_days)





    max_voucher_no = cls.objects.filter(company=company).aggregate(Max('voucher_no'))['voucher_no__max']
    if max_voucher_no:
        return max_voucher_no + 1
    else:
        return 1


def empty_to_zero(o):
    if o == '':
        return 0
    if o is None:
        return 0
    return o


def validate_row(rows, args):
    temp = []
    for item in rows:
        if int(item.get(args)) in temp:
            return False
        else:
            temp.append(int(item.get(args)))
    return True

