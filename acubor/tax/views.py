import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from ledger.models import TaxScheme
from ledger.serializers import TaxSchemeSerializer
from ledger.forms import TaxSchemeForm


@login_required
def list_tax_schemes(request):
    tax_schemes = TaxScheme.objects.filter(company=request.user.currently_activated_company)
    return render(request, 'list_tax_schemes.html', {'objects': tax_schemes})


@login_required
def schemes_as_json(request):
    schemes = TaxScheme.objects.filter(company=request.user.currently_activated_company)
    items_data = TaxSchemeSerializer(schemes).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


@login_required
def delete_tax_scheme(request, id):
    object = get_object_or_404(TaxScheme, id=id, company=request.user.currently_activated_company)
    object.delete()
    return redirect('/tax/schemes/')


@login_required
def tax_scheme_form(request, id=None):
    if id:
        obj = get_object_or_404(TaxScheme, id=id, company=request.user.currently_activated_company)
        scenario = 'Update'
    else:
        obj = TaxScheme(company=request.user.currently_activated_company)
        scenario = 'Create'
    if request.POST:
        form = TaxSchemeForm(data=request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.company = request.user.currently_activated_company
            obj.save()
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': TaxSchemeSerializer(obj).data})
            return redirect('/tax/schemes/')
    else:
        form = TaxSchemeForm(instance=obj)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'dashboard.html'
    return render(request, 'tax_scheme_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })
