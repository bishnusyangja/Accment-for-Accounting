from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from core.models import CompanySetting, VoucherSetting
from core.forms import CompanySettingsForm, VoucherSettingsForm


@login_required
def company_settings(request):
    msg = None
    company_setting = CompanySetting.objects.get(company=request.user.currently_activated_company)
    if request.POST:
        form = CompanySettingsForm(data=request.POST, instance=company_setting)
        if form.is_valid():
            form.save()
            msg = "Saved!"
    else:
        form = CompanySettingsForm(instance=company_setting)
    return render(request, 'company_settings.html', {'form': form, "msg":msg})

@login_required
def default_homepage(request):
    comp_sett = CompanySetting.objects.get(company=request.user.currently_activated_company)
    if comp_sett.default_home_page == "Dashboard":
        return redirect('/application/')
    if comp_sett.default_home_page == "Company Settings":
        return redirect('/settings/company')

@login_required
def voucher_settings(request):
    voucher_setting = VoucherSetting.objects.get(company=request.user.currently_activated_company)
    if request.POST:
        form = VoucherSettingsForm(data=request.POST, instance=voucher_setting)
        if form.is_valid():
            form.save()
    else:
        form = VoucherSettingsForm(instance=voucher_setting)
    return render(request, 'voucher_settings.html', {'form': form})
