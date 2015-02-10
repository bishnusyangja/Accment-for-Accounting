from django import forms
from django.core.urlresolvers import reverse_lazy
from lib import KOModelForm
from mptt.forms import TreeNodeChoiceField
from models import Item, Category, Unit
from models import PhysicalStockVoucher


class PhysicalStockForm(KOModelForm):
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(PhysicalStockForm, self).__init__(*args, **kwargs)

    def clean_voucher_no(self):
        try:
            existing = PhysicalStockVoucher.objects.get(voucher_no=self.cleaned_data['voucher_no'],
                                                        company=self.company)
            if self.instance.id is not existing.id:
                raise forms.ValidationError("The voucher no. " + str(
                    self.cleaned_data['voucher_no']) + " is already in use. Suggested voucher no. has been provided!")
            return self.cleaned_data['voucher_no']
        except PhysicalStockVoucher.DoesNotExist:
            return self.cleaned_data['voucher_no']

    class Meta:
        model = PhysicalStockVoucher
        exclude = ['company', 'status']


class ItemForm(KOModelForm):
    category = TreeNodeChoiceField(Category.objects.all(), empty_label=None,
                                   widget=forms.Select(attrs={'class': 'select2 form-control', 'data-name': 'Category',
                                                              'data-url': reverse_lazy(
                                                                  'create_inventory_category')}))
    unit = forms.ModelChoiceField(Unit.objects.all(), required=False, widget=forms.Select(
        attrs={'class': 'select2 form-control', 'data-name': 'Unit',
               'data-url': reverse_lazy('create_unit')}))

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(company=self.company)
        self.fields['unit'].queryset = Unit.objects.filter(company=self.company)
        self.fields['name'].widget.attrs['class']='form-control'

    class Meta:
        model = Item
        exclude = ['company', 'account']

    # def clean(self):
    #     """ This is the form's clean method, not a particular field's clean method """
    #     cleaned_data = self.cleaned_data
    #
    #     name = cleaned_data.get('name')
    #
    #     # try:
    #     #     obj = Item.objects.get(name=name, company=self.company)
    #     #     if not obj.id == self.instance.id:
    #     #         raise forms.ValidationError("Item name already exists.")
    #     # except Item.DoesNotExist:
    #     #     pass
    #
    #     # Always return the full collection of cleaned data
    #     return cleaned_data


class CategoryForm(KOModelForm):
    parent = TreeNodeChoiceField(Category.objects.all(), required=False,
                                 widget=forms.Select(attrs={'class': 'select2', 'data-name': 'Category',
                                                            'data-url': reverse_lazy(
                                                                'create_inventory_category')}))

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.filter(company=self.company)

    class Meta:
        model = Category
        exclude = ['company']

    # def clean(self):
    #     """ This is the form's clean method, not a particular field's clean method """
    #     cleaned_data = self.cleaned_data
    #
    #     name = cleaned_data.get('name')
    #
    #     if Category.objects.filter(name=name, company=self.company).count() > 0:
    #         raise forms.ValidationError("Category name already exists.")
    #
    #     # Always return the full collection of cleaned data.
    #     return cleaned_data


class UnitForm(KOModelForm):
    class Meta:
        model = Unit
        exclude = ['company']
