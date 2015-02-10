from django import forms
from models import Company
from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from captcha.fields import ReCaptchaField
from passwords.fields import PasswordField
import datetime


TYPES_OF_BUSINESS = (('Convenience Store', 'Convenience Store',),
                     ('Gas Station and Store', 'Gas Station and Store',),
                     # ('Gas Station', 'Gas Station',),
                     ('Service Related Industries', 'Service Related Industries',),
                     # ('Retail Trading Industries', 'Retail Trading Industries',),
                     # ('Wholesale Trading Industries', 'Wholesale Trading Industries',),
                     # ('Manufacturing Industries', 'Manufacturing Industries',),
                     # ('Financial and Allied Industries', 'Financial and Allied Industries',),
                    )
FUEL_OWNED_BY = (('Self', 'Self',), ('Gas Company', 'Gas Company',), )


class CompanyForm(forms.Form):
    name = forms.CharField(max_length=50)
    type_of_business = forms.ChoiceField(choices=TYPES_OF_BUSINESS, label='Type of Business')
    street_address_1 = forms.CharField(max_length=100)
    street_address_2 = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=2)
    zip_code = forms.CharField(max_length=5)
    books_start_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'date-picker-full'}), initial=str(datetime.date.today().strftime('%m/%d/%Y')))
    financial_year_start_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'date-picker'}),
                                                initial='01/01')
    books_closing_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'date-picker'}), initial='12/31')

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Company\'s official name'
        self.fields['street_address_1'].widget.attrs['placeholder'] = 'Street Address Line #1'
        self.fields['street_address_2'].widget.attrs['placeholder'] = 'Street Address Line #2'
        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['state'].widget.attrs['placeholder'] = 'State'
        self.fields['zip_code'].widget.attrs['placeholder'] = 'Zip Code'
        self.fields['name'].widget.attrs['style'] = 'width:95%'
        self.fields['street_address_1'].widget.attrs['style'] = 'width:95%'
        self.fields['street_address_2'].widget.attrs['style'] = 'width:95%'
        self.fields['city'].widget.attrs['style'] = 'width:95%'
        self.fields['state'].widget.attrs['style'] = 'width:95%'
        self.fields['zip_code'].widget.attrs['style'] = 'width:95%'

    def clean_name(self):
        """
        Validate that the name is alphanumeric and is not already
        in use.

        """
        existing = Company.objects.filter(name__iexact=self.cleaned_data['name'])
        if existing.exists():
            raise forms.ValidationError(_("A company with that name already exists."))
        else:
            return self.cleaned_data['name']

    def clean_state(self):
        """
        Validate that the state is 2 characters long.

        """
        if len(self.cleaned_data['state']) > 2:
            raise forms.ValidationError(_("State should be only 2 characters long."))
        else:
            return self.cleaned_data['state']


class UserRegistrationForm(RegistrationForm):
    full_name = forms.CharField(widget=forms.TextInput())
    captcha = ReCaptchaField()
    password1 = PasswordField()
    password2 = PasswordField()

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-enter Password'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['username'].widget.attrs['style'] = 'width:95%'
        self.fields['full_name'].widget.attrs['style'] = 'width:95%'
        self.fields['password1'].widget.attrs['style'] = 'width:95%'
        self.fields['password2'].widget.attrs['style'] = 'width:95%'
        self.fields['email'].widget.attrs['style'] = 'width:95%'
        self.fields.keyOrder = ['full_name', 'username', 'email', 'password1', 'password2', 'captcha']

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        existing = get_user_model().objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        return self.cleaned_data['email']


    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        # self.cleaned_data['username'] = self.cleaned_data['email']
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

    class Meta:
        model = get_user_model()
