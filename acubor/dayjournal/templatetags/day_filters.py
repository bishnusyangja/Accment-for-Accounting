from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.filter
def index(value, arg):
    return value[arg]


@register.filter
def total(value):
    if type(value) == list:
        return sum(value)
    else:
        return value

@register.filter
def cumsumtot(val, ind):
    tot = 0
    for i in range(ind+1):
        tot += sum(index(val,i))
    return tot


@register.filter
def subtracting(value, arg):
    return value - arg


@register.filter
@stringfilter
def negativeformat(value):
    if len(value) == 0:
        return value
    if value[0] == '-':
        return '<span style="color:red;">' + '(' + value[1:] + ')' + '</span>'
    else:
        return '%s' % (value)


@register.filter
def grand_total(item):
    tot = 0
    for sc in item.rows.all():
        if sc.addition is not None:
            tot += (sc.out_count - sc.in_count + sc.addition)*sc.rate
        else:
            tot += (sc.out_count - sc.in_count)*sc.rate
    return tot


@register.filter
def adding(value, arg):
    return float(value) + float(arg)


@register.filter
def total_short(value):
    tot = 0.0
    for item in value:
        res = item.get_closing_balance() - float(item.cash_actual)
        if res < 0.0:
            tot += -1*res
    return tot


@register.filter
def total_excess(value):
    tot = 0.0
    for item in value:
        res = item.get_closing_balance() - float(item.cash_actual)
        if res > 0.0:
            tot += res
    return tot


@register.filter
def positive(value):
    if value < 0:
        return -1*value
    else:
        return value

