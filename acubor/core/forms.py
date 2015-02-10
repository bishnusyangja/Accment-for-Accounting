from django import forms

from core.models import CompanySetting, Currency, VoucherSetting


class CompanySettingsForm(forms.ModelForm):
    class Meta:
        model = CompanySetting
        exclude = ['company', 'company_type', 'financial_year_starts_on', 'financial_year_ends_on',
                   'current_financial_year_started_on', 'registered_date', ]


class VoucherSettingsForm(forms.ModelForm):
    class Meta:
        model = VoucherSetting
        exclude = ['company']
