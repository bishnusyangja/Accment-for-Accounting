from django import forms

from payroll.models import Employee, AttendanceParameter
from users.models import User, Role


class EmployeeForm(forms.ModelForm):
    user = forms.ModelChoiceField(User.objects.all(), widget=forms.Select(attrs={'class': 'select2'}))

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        self.scenario = kwargs.pop('scenario', None)
        self.user = kwargs.pop('user', None)

        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        if not self.user:
            self.fields['user'].queryset = User.objects.filter(
                id__in=Role.objects.filter(company=self.company).values_list('user', flat=True).distinct())

    class Meta:
        model = Employee
        exclude = ['account', 'company']

    def clean_tax_id(self):
        data = self.cleaned_data['tax_id']
        data = str(data)
        if data:
            if not data.isdigit():
                raise forms.ValidationError('Tax id must be in digits.')
        return data


class AttendanceParameterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AttendanceParameterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AttendanceParameter
        exclude = ['company', 'abs']

    def validate(self, field):
        data = self.cleaned_data[field]
        if data != 0:
            if not data:
                raise forms.ValidationError('Empty is not allowed.')
        if data > 1 or data < 0:
            raise forms.validationError('Only number between 0 to 1 is allowed.')
        return data

    def clean_early_leave(self):
        ret = self.validate('early_leave')
        return ret

    def clean_full_att(self):
        ret = self.validate('full_att')
        return ret

    def clean_late_att(self):
        ret = self.validate('late_att')
        return ret

    def clean_half_att(self):
        ret = self.validate('half_att')
        return ret

