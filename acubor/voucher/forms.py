from django import forms
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy

from lib import KOModelForm, ExtFileField
# from core.models import Currency
from ledger.models import Party, Account
from voucher.models import Invoice, PurchaseVoucher, CashReceipt, CashPayment


class InvoiceForm(KOModelForm):
    party = forms.ModelChoiceField(Account.objects.all(), empty_label='Choose a customer',
                                   widget=forms.Select(attrs={'class': 'select2 placehold', 'data-name': 'Customer',
                                                              'data-url': reverse_lazy('create_customer'),
                                   }),
                                   label='To')
    # currency = forms.ModelChoiceField(Currency.objects.all(), empty_label=None,
    #                                   widget=forms.Select(attrs={'class': 'select2'}))

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['party'].queryset = Account.objects.filter(company=self.company)
        self.fields['party'].widget.attrs['style'] = 'width:80px;'
        self.fields['voucher_no'].widget.attrs['style'] = 'width:40px;'

    def clean_voucher_no(self):
        try:
            existing = Invoice.objects.get(voucher_no=self.cleaned_data['voucher_no'], company=self.company)
            if self.instance.id is not existing.id:
                raise forms.ValidationError("The voucher no. " + str(
                    self.cleaned_data['voucher_no']) + " is already in use. Suggested voucher no. has been provided!")
            return self.cleaned_data['voucher_no']
        except Invoice.DoesNotExist:
            return self.cleaned_data['voucher_no']

    class Meta:
        model = Invoice
        exclude = ['company', 'status']


class PurchaseVoucherForm(KOModelForm):
    party = forms.ModelChoiceField(Account.objects.all(), empty_label=None,
                                   widget=forms.Select(attrs={'class': 'select2', 'data-name':'Vendor',
                                   'data-url': reverse_lazy('create_suppliers')}), label='From')

    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': 'mm/dd/yyyy'}))
    due_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker', 'data-date-format': 'mm/dd/yyyy'}))

    attachment = ExtFileField(
        label='Add an attachment',
        help_text='',
        required=False,
        ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
    )

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(PurchaseVoucherForm, self).__init__(*args, **kwargs)
        self.fields['voucher_no'].widget.attrs['class'] = 'short-input'
        self.fields['reference'].widget.attrs['class'] = 'short-input'
        self.fields['party'].queryset = Account.objects.filter(Q(category__name='Cash Account') | Q(category__name='Bank Account') | Q(category__name='Suppliers'), company=self.company)

    def clean_voucher_no(self):
        try:
            existing = PurchaseVoucher.objects.get(voucher_no=self.cleaned_data['voucher_no'], company=self.company)
            if self.instance.id is not existing.id:
                raise forms.ValidationError("The voucher no. " + str(
                    self.cleaned_data['voucher_no']) + " is already in use. Suggested voucher no. has been provided!")
            return self.cleaned_data['voucher_no']
        except PurchaseVoucher.DoesNotExist:
            return self.cleaned_data['voucher_no']

    class Meta:
        model = PurchaseVoucher
        exclude = ['company', 'pending_amount', 'total_amount', 'status']


class CashReceiptForm(KOModelForm):
    cash_account = forms.ModelChoiceField(Account.objects.filter(category__name='Cash Account'), empty_label=None,
                                          widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Cash Account',
                                                                     'data-url': "/ledger/create/?category_id=31"}),
                                          label='Cash Account')

    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))

    attachment = ExtFileField(
        label='Add an attachment',
        help_text='add an attachment',
        required=False,
        ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
    )

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(CashReceiptForm, self).__init__(*args, **kwargs)
        self.fields['cash_account'].queryset = Account.objects.filter(company=self.company,
                                                                      category__name='Cash Account').order_by('name')

    def clean_voucher_no(self):
        try:
            existing = CashReceipt.objects.get(voucher_no=self.cleaned_data['voucher_no'], company=self.company)
            if self.instance.id is not existing.id:
                raise forms.ValidationError("The voucher no. " + str(
                    self.cleaned_data['voucher_no']) + " is already in use. Suggested no. has been provided.")
            return self.cleaned_data['voucher_no']
        except CashReceipt.DoesNotExist:
            return self.cleaned_data['voucher_no']

    class Meta:
        model = CashReceipt
        exclude = ['company', 'status']


class CashPaymentForm(KOModelForm):
    cash_account = forms.ModelChoiceField(Account.objects.filter(category__name='Cash Account'), empty_label=None,
                                          widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Cash Account',
                                                                     'data-url': "/ledger/create/?category_id=31"}),
                                          label='Cash Account')

    date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-picker'}))

    attachment = ExtFileField(
        label='Add an attachment',
        help_text='add an attachment',
        required=False,
        ext_whitelist=('.jpg', '.png', '.gif', '.tif', '.pdf')
    )

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(CashPaymentForm, self).__init__(*args, **kwargs)
        self.fields['cash_account'].queryset = Account.objects.filter(company=self.company,
                                                                      category__name='Cash Account').order_by('name')

    def clean_voucher_no(self):
        try:
            existing = CashPayment.objects.get(voucher_no=self.cleaned_data['voucher_no'], company=self.company)
            if self.instance.id is not existing.id:
                raise forms.ValidationError("The voucher no. " + str(
                    self.cleaned_data['voucher_no']) + " is already in use. Suggested no. has been provided.")
            return self.cleaned_data['voucher_no']
        except CashPayment.DoesNotExist:
            return self.cleaned_data['voucher_no']

    class Meta:
        model = CashPayment
        exclude = ['company', 'status']
