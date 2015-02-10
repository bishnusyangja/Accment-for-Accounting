from django import template

register = template.Library()

@register.filter
def index(value, i):
    result = None
    if type(value) == list:
        result = value[i]
    return result

@register.filter
def keyval(value, arg):
    return value[arg]

@register.filter
def filename(my_string):
    my_string = str(my_string)
    array = my_string.split('/')
    return array[len(array)-1]

@register.filter
def get_purchase_amount(arg):
    tot =  arg.unit_price * arg.quantity
    if arg.discount:
        return tot*(1-arg.discount/100.0)
    else:
        return tot

@register.filter
def get_purchase_total(arg):
    tot = 0
    for item in arg.particulars.all():
        tot += get_purchase_amount(item)
    return tot


@register.filter
def typeof(item):
    return item.__class__.__name__