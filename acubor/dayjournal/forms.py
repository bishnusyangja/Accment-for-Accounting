__author__ = 'sarvagya'
from lib import KOModelForm
from dayjournal.models import ScratchOffLatest
from django.core.urlresolvers import reverse_lazy
from django import forms
from payroll.views import hr_24


class ScratchOffLatestForm(KOModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))

    def clean(self):
        cleaned_data = super(ScratchOffLatestForm, self).clean()
        in_time = cleaned_data.get('in_time')
        out_time = cleaned_data.get('out_time')
        new_in_time = [int(item) for item in hr_24(in_time).split(":")]
        new_out_time = [int(item) for item in hr_24(out_time).split(":")]
        if new_in_time[0] > new_out_time[0]:
            raise forms.ValidationError("Out time cannot be smaller than In Time")
        elif new_in_time[0] == new_out_time[0] and new_in_time[1] > new_out_time[1]:
            raise forms.ValidationError("Out time cannot be smaller than In Time")
        else:
            return cleaned_data


    def __init__(self,*args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(ScratchOffLatestForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ScratchOffLatest
        exclude = ['company']