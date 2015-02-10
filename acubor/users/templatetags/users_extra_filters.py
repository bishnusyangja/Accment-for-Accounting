from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

# @register.filter
# def get_settings(request):
#     try:
#         return {
#             'decimal_places': request.user.currently_activated_company.settings.decimal_places,
#             'number_comma_system': request.user.currently_activated_company.settings.number_comma_system
#         }
#     except:
#         return {}

@register.filter
@stringfilter
def negativeformat(value):
    if len(value) == 0:
        return value
    if value[0] == '-':
        return '<span style="color:red;">' + '(' + value[1:] + ')' + '</span>'
    else:
        return '%s' % (value)
