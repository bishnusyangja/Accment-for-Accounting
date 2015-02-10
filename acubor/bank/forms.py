from django import forms
from django.core.urlresolvers import reverse_lazy

from lib import KOModelForm, ExtFileField
from models import BankAccount,  BankDeposit, BankPayment
from ledger.models import Account


class BankAccountForm(KOModelForm):
    class Meta:
        model = BankAccount
        exclude = ['company', 'account']


class BankDepositForm(KOModelForm):
    bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank Account'), empty_label=None,
                                          widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Bank Account',
                                                                     'data-url': reverse_lazy('create_bank_account')}),
                                          label='Bank Account')

    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))

    attachment = ExtFileField(
        label='Add an attachment',
        help_text='add an attachment',
        required=False,
        ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
    )

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(BankDepositForm, self).__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = Account.objects.filter(company=self.company,
                                                                      category__name='Bank Account').order_by('name')
    def clean_voucher_no(self):
        try:
            existing = BankDeposit.objects.get(voucher_no=self.cleaned_data['voucher_no'], company=self.company)
            if self.instance.id is not existing.id:
                raise forms.ValidationError("The voucher no. " + str(
                    self.cleaned_data['voucher_no']) + " is already in use. Suggested no. has been provided.")
            return self.cleaned_data['voucher_no']
        except BankDeposit.DoesNotExist:
            return self.cleaned_data['voucher_no']

    class Meta:
        model = BankDeposit
        exclude = ['company', 'status']


class BankPaymentForm(KOModelForm):
    bank_account = forms.ModelChoiceField(Account.objects.filter(category__name='Bank Account'), empty_label=None,
                                          widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Bank Account',
                                                                     'data-url': reverse_lazy('create_bank_account')}),
                                          label='Bank Account')

    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))

    attachment = ExtFileField(
        label='Add an attachment',
        help_text='add an attachment',
        required=False,
        ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
    )

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(BankPaymentForm, self).__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = Account.objects.filter(company=self.company,
                                                                      category__name='Bank Account').order_by('name')
    def clean_voucher_no(self):
        try:
            existing = BankPayment.objects.get(voucher_no=self.cleaned_data['voucher_no'], company=self.company)
            if self.instance.id is not existing.id:
                raise forms.ValidationError("The voucher no. " + str(
                    self.cleaned_data['voucher_no']) + " is already in use. Suggested no. has been provided.")
            return self.cleaned_data['voucher_no']
        except BankPayment.DoesNotExist:
            return self.cleaned_data['voucher_no']

    class Meta:
        model = BankPayment
        exclude = ['company', 'status']
