from django import forms

from models import TaxScheme


class TaxSchemeForm(forms.ModelForm):
    class Meta:
        model = TaxScheme
        exclude = ['company']
