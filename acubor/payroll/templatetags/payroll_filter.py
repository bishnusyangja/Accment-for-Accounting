
from django import template
from itertools import izip_longest
# from core.models import CompanySetting

register = template.Library()

@register.filter
def multiply(value, arg):
    if not value:
        value = 0
    if not arg:
        arg = 0
    return round(float(value)*float(arg), 3)

@register.filter
def subtract(value, arg):
    if value is None:
        value = 0.0
    if arg is None:
        arg = 0.0
    return round(value-arg, 2)

@register.filter
def dash(value):
    if value is None:
        return '-'
    else:
        return round(value, 2)

@register.filter
def zero_f_none(value):
    if value is None:
        return 0.0
    else:
        return round(value, 2)

@register.filter
def absolute(value):
    if value < 0:
        return -1*value
    else:
        return round(value, 2)

@register.filter
def maxi(value, arg):
    if len(value) < len(arg):
        ret = len(arg)
    else:
        ret = len(value)
    if ret > 1:
        ret += 1
    return ret


@register.filter
def enm(value):
    return enumerate(value)

@register.filter
def combine(value, arg):
    a = izip_longest(value,arg, fillvalue='-')
    return list(a)

@register.filter
def val(value, arg):
    return value[arg-1]

@register.filter
def total(value):
    tot = 0.0
    for item in value:
        tot += item.amount
    return round(tot, 2)

@register.filter
def result(value, arg):
    return round(total(value) - total(arg), 2)

@register.filter
def sb(value, arg):
    a = time_format(value)
    a = not_am_pm(a)
    b = time_format(arg)
    b = not_am_pm(b)
    x = a.split(':')
    y = b.split(':')
    r = int((x[0]-y[0])*60 + x[1]-y[1])
    return r

@register.filter
def ad(value, arg):
    a = time_format(value)
    a = not_am_pm(a)
    b = time_format(arg)
    b = not_am_pm(b)
    x = a.split(':')
    y = b.split(':')
    r = int((x[0]+y[0])*60 + x[1]+y[1])
    m = r % 60
    h = r / 60
    return h + ':' + m


@register.filter
def index(value, arg):
    return value[arg]

@register.filter
def work_time(value):
    a1 = not_a_p(value.in_time1)
    b1 = not_a_p(value.out_time1)
    a2 = not_a_p(value.in_time2)
    b2 = not_a_p(value.out_time2)
    x = aad(a1, a2)
    y = aad(b1, b2)
    return ssb(y, x)


def not_am_pm(value):
    if value.find('pm'):
        value.replace('pm', '')
    if value.find('PM'):
        value.replace('PM', '')
    if value.find('Pm'):
        value.replace('Pm', '')
    if value.find('pM'):
        value.replace('pM', '')
    if value.find('am'):
        value.replace('am', '')
    if value.find('AM'):
        value.replace('AM', '')
    if value.find('Am'):
        value.replace('Am', '')
    if value.find('aM'):
        value.replace('aM', '')
    return value


def time_format(value):
    if value.index('pm') or value.index('Pm') or value.index('pM') or value.index('PM'):
        a = value.split(':')
        a[0] += 12
        value = a[0] + ':' + a[1]
    return value


def not_a_p(value):
    value = str(value)
    if value.find('a.m.'):
        value = value.replace('a.m.', '')
    if value.find('p.m.'):
        value = value.replace('p.m.', '')
        a = value.split(':')
        a[0] = 12 + int(a[0])
        value = str(a[0]) + ':' + str(a[1])
    return value

@register.filter
def ssb(value, arg):
    t = int(value) - int(arg)
    h = t / 60
    m = t % 60
    return str(h) + ':' + str(m)


@register.filter
def aad(value, arg):
    value = str(value)
    arg = str(arg)
    x = value.split(':')
    if len(x) == 1:
        x.append(0)
    y = arg.split(':')
    if len(y) == 1:
        y.append(0)
    r = int(x[0])*60+int(y[0])*60 + int(x[1])+int(y[1])
    return round(float(r), 2)


@register.filter
def joda(value, arg):
    return round(float(value)+float(arg), 2)


@register.filter
def spliturl(value):
    return value.split('/')[-2]


# @register.filter
# def fnum(value):
#     value = str(value)
#     # comma system 1,120,000s
#     result = ''
#     value = value.split('.')[0]
#     l = len(value)
#     for i in range(l):
#         value[l-i-1]


