from django import template


register = template.Library()

@register.filter
def fnum(val):
    # print val
    if val < 0:
        # print val
        temp = "%.2f" % (-1*val)
        return temp + ' (Cr)'
    else:
        temp = "%.2f" % val
        return temp + ' (Dr)'

@register.filter
def fornum(value):
    if value is '':
        return value

    value = str(value)
    value = value.split('.')
    val = value[0]
    l = len(val)
    while(1):
        l -= 3
        if l < 1:
            break
        val = val[:l]+','+val[l:]
    if len(value) > 1:
        value = val + '.' + value[1]

    return value


@register.filter
def keep_account(transactions, account):
    return [transaction for transaction in transactions if
            transaction.account.id == account.id]

@register.filter
def decimalise(val):
    val = str(val)
    val = val.split('.')
    temp = val[0]
    if len(val) == 1:
        temp += '.00'
    else:
        if len(val[1]) == 1:
            temp = temp + '.' + val[1] + '0'
        else:
            temp = temp + '.' + val[1]
    return temp