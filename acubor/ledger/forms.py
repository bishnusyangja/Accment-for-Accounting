from django import forms
from django.core.urlresolvers import reverse_lazy
from mptt.forms import TreeNodeChoiceField
from django.core.validators import validate_email
from lib import KOModelForm
# from lib import zero_for_none
from models import Account, Category, Party, BankAccountDetail, PartyAccountDetail, AccountTaxDetail, \
    InterestScheme, TaxScheme
import re


class AccountForm(KOModelForm):
    category = TreeNodeChoiceField(Category.objects.all(),
                                   widget=forms.Select(attrs={'class': 'select2 form-control', 'data-name': 'Category',
                                                              'data-url': reverse_lazy('create_category')}))

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        self.scenario = kwargs.pop('scenario', None)
        self.category = kwargs.pop('category', None)
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        if not self.category:
            self.fields['category'].queryset = Category.objects.filter(company=self.company)

    class Meta:
        model = Account
        exclude = ['company', 'is_default', 'code', 'interest_scheme', 'current_cr', 'current_dr',
                   'opening_as_on_date']

    def clean(self):
        """ This is the form's clean method, not a particular field's clean method """
        cleaned_data = self.cleaned_data
        opening_dr = cleaned_data.get('opening_dr')
        opening_cr = cleaned_data.get('opening_cr')

        if opening_cr and opening_dr:
            if opening_dr != 0 and opening_cr != 0:
                raise forms.ValidationError('You cannot enter both opening debit and opening credit amounts.')
        return cleaned_data

    def clean_opening_cr(self):
        value = self.cleaned_data.get('opening_cr')
        if value and value < 0:
            raise forms.ValidationError('Amount cannot be negative.')
        elif not value:
            value = 0.00
        return value

    def clean_opening_dr(self):
        value = self.cleaned_data.get('opening_dr')
        if value and value < 0:
            raise forms.ValidationError('Amount cannot be negative.')
        elif not value:
            value = 0.00
        return value

    def clean_name(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data.get('name')

        try:
            obj = Account.objects.get(name=name, company=self.company)
            if not obj.id == self.instance.id:
                raise forms.ValidationError("Account name already exists.")
        except Account.DoesNotExist:
            pass

        objs = Account.objects.filter(name__in=["Cash Account", "Paid in Capital", "Drawings", "Opening",
                                                "Profit/Loss", "Opening Stock", "Closing Stock", ]
                                      , company=self.company)
        ids = [obj.id for obj in objs]
        try:
            name_check = Account.objects.get(id=self.instance.id, company=self.company).name
            if self.instance.id in ids and not name == name_check:
                raise forms.ValidationError("This Account is a default Account. Its name can't be edited.")
        except Account.DoesNotExist:
            pass
        return name

    def clean_category(self):
        cleaned_data = self.cleaned_data
        category = cleaned_data.get('category')
        objs = Account.objects.filter(name__in=["Cash Account", "Paid in Capital", "Drawings", "Opening",
                                                "Profit/Loss", "Opening Stock", "Closing Stock", ]
                                      , company=self.company)
        ids = [obj.id for obj in objs]
        try:
            category_check = Account.objects.get(id=self.instance.id, company=self.company).category
            if self.instance.id in ids and not category == category_check:
                raise forms.ValidationError("This Account is a default Account. Its category can't be edited.")
        except Account.DoesNotExist:
            pass
        return category

class BankAccountDetailForm(KOModelForm):
    def __init__(self, *args, **kwargs):

        super(BankAccountDetailForm, self).__init__(*args, **kwargs)
        self.fields['bank_name'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = BankAccountDetail
        exclude = ['account', 'company']

    def clean_bank_name(self):
        clened_data = self.cleaned_data
        bn = clened_data.get('bank_name')
        if not bn:
            raise forms.ValidationError("Bank Name is Required.")
        return bn

    def clean_email_address(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('bank_email_address')
        pattern = r'[^@]+@[^@]+\.[^@]+'
        # if not email:
        if email and not re.match(pattern, email):
            raise forms.ValidationError("Enter email address. This is not valid.")
        return email

    def clean_contact_no(self):
        cleaned_data = self.cleaned_data
        number = cleaned_data.get('contact_no')
        pattern = r'^[0-9]+$'
        if number and not re.match(pattern, number):
            raise forms.ValidationError("Enter contact number. This is not valid.")
        return number


class PartyAccountDetailForm(KOModelForm):
    class Meta:
        model = PartyAccountDetail
        exclude = ['account', 'company']

    def clean_tin_no(self):
        cleaned_data = self.cleaned_data
        number = cleaned_data.get('tin_no')
        pattern = r'^[0-9]+$'

        if number and not re.match(pattern, number):
            raise forms.ValidationError("Enter TIN number. This is not valid.")
        return number

    def clean_email_address(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('party_email_address')
        pattern = r'[^@]+@[^@]+\.[^@]+'

        if email and not re.match(pattern, email):
            raise forms.ValidationError("Enter email address. This is not valid.")
        return email


class AccountTaxDetailForm(KOModelForm):
    pri_tax_scheme = forms.ModelChoiceField(TaxScheme.objects.all(), widget=forms.Select(attrs={'class': 'select2',
                                                                                                'data-name': 'Tax Scheme',
                                                                                                'data-url': reverse_lazy(
                                                                                                    'create_tax_scheme')}))
    sec_tax_scheme_1 = forms.ModelChoiceField(TaxScheme.objects.all(), widget=forms.Select(attrs={'class': 'select2',
                                                                                                  'data-name': 'Tax Scheme',
                                                                                                  'data-url': reverse_lazy(
                                                                                                      'create_tax_scheme')}))
    sec_tax_scheme_2 = forms.ModelChoiceField(TaxScheme.objects.all(), widget=forms.Select(attrs={'class': 'select2',
                                                                                                  'data-name': 'Tax Scheme',
                                                                                                  'data-url': reverse_lazy(
                                                                                                      'create_tax_scheme')}))
    sec_tax_scheme_3 = forms.ModelChoiceField(TaxScheme.objects.all(), widget=forms.Select(attrs={'class': 'select2',
                                                                                                  'data-name': 'Tax Scheme',
                                                                                                  'data-url': reverse_lazy(
                                                                                                      'create_tax_scheme')}))

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(AccountTaxDetailForm, self).__init__(*args, **kwargs)
        self.fields['pri_tax_scheme'].queryset = TaxScheme.objects.filter(company=self.company)
        self.fields['sec_tax_scheme_1'].queryset = TaxScheme.objects.filter(company=self.company)
        self.fields['sec_tax_scheme_2'].queryset = TaxScheme.objects.filter(company=self.company)
        self.fields['sec_tax_scheme_3'].queryset = TaxScheme.objects.filter(company=self.company)

    class Meta:
        model = AccountTaxDetail
        exclude = ['account', 'company']


class InterestSchemeForm(KOModelForm):
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        self.scenario = kwargs.pop('scenario', None)
        super(InterestSchemeForm, self).__init__(*args, **kwargs)
        self.fields['collection_ledger'].widget.attrs['class'] = 'select2'
        self.fields['collection_ledger'].queryset = Account.objects.filter(company=self.company)

    class Meta:
        model = InterestScheme
        exclude = ['company']


class PartyForm(KOModelForm):
    class Meta:
        model = Party
        exclude = ['company', 'customer_account', 'supplier_account']


class CategoryForm(KOModelForm):
    parent = TreeNodeChoiceField(Category.objects.all(), empty_label=None,
                                 widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Category',
                                                            'data-url': reverse_lazy(
                                                                'create_category')}))

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.filter(company=self.company)

    class Meta:
        model = Category
        exclude = ['company']
        fields = ['name', 'parent', 'description', 'is_default']

    def clean(self):
        """ This is the form's clean method, not a particular field's clean method """
        cleaned_data = self.cleaned_data

        name = cleaned_data.get('name')

        categories_check_list = Category.objects.filter(name=name, company=self.company)
        if categories_check_list.count() > 0:
            if categories_check_list[0].id != cleaned_data.get('id'):
                raise forms.ValidationError("Category name already exists.")
                # category_accounts = categories_check_list[0].accounts
                # for each in category_accounts:
                # try:
                #         transactionss = Transaction.objects.filter(account=each)
                #         if len(transactionss) > 0:
                #             raise forms.ValidationError(
                #                 "This Category has Accounts that have transactions. Please delete the vouchers initiating those transactions first.")
                #     except Account.DoesNotExist:
                #         pass

        # Always return the full collection of cleaned data.
        return cleaned_data


class TaxSchemeForm(KOModelForm):
    collection_ledger = forms.ModelChoiceField(Account.objects.all(),
                                               widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Account',
                                                                          'data-url': reverse_lazy(
                                                                              'create_account')}))

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        self.scenario = kwargs.pop('scenario', None)
        super(TaxSchemeForm, self).__init__(*args, **kwargs)
        self.fields['collection_ledger'].queryset = Account.objects.filter(company=self.company)

        if self.scenario == 'Update':
            pass

    class Meta:
        model = TaxScheme
        exclude = ['company', 'is_default']

    def clean_percent(self):
        cleaned_data = self.cleaned_data
        percent = cleaned_data.get('percent')

        if percent >= 100:
            raise forms.ValidationError('Percent must be less than 100')
        if percent < 0:
            raise forms.ValidationError('Percent must be positive number')
        return percent
