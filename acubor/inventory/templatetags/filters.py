import copy
import json
from datetime import date, timedelta

from django.utils.datastructures import SortedDict
from django.core import serializers
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.db.models import Model
from django import template
from django.template import resolve_variable, NodeList
from django.contrib.auth.models import Group


register = template.Library()


def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    # elif isinstance(obj, ...):
    #     return ...
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))


@register.filter
def jsonify(object):
    if isinstance(object, QuerySet):
        return serializers.serialize('json', object)
    if isinstance(object, Model):
        model_dict = object.__dict__
        del model_dict['_state']
        return mark_safe(json.dumps(model_dict))
    return mark_safe(json.dumps(object, default=handler))


@register.filter
def user_to_json(user):
    if hasattr(user, '_wrapped') and hasattr(user, '_setup'):
        if user._wrapped.__class__ == object:
            user._setup()
        user = user._wrapped
    user_dict = {'id': user.id, 'username': user.username}
    return mark_safe(json.dumps(user_dict))


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def if_not_none(obj):
    if obj is None:
        return ''
    return obj


@register.filter
def if_not_zero(obj):
    if obj == 0:
        return ''
    return obj


@register.filter
def subtract(value, arg):
    if value is None:
        value = 0
    if arg is None:
        arg = 0
    return value - arg


@register.simple_tag
def yesterday():
    today = date.today()
    return today - timedelta(days=1)


@register.filter
def get_settings(request):
    try:
        return {
            'decimal_places': request.user.currently_activated_company.settings.decimal_places,
            'number_comma_system': request.user.currently_activated_company.settings.number_comma_system
        }
    except:
        return {}


@register.filter
def day_journal_id(obj):
    #TODO DB Optimisation
    try:
        source = obj.content_type.get_object_for_this_type(id=obj.model_id)
    except:
        return None
    try:
        return source.day_journal.id
    except:
        return source.id


@register.filter
def refine_voucher_type(the_type):
    if the_type[-4:] == ' row':
        the_type = the_type[:-3]
    if the_type[-11:] == ' particular':
        the_type = the_type[:-10]
    return the_type.title()


@register.filter
def url_for_content(obj):
    #TODO DB Optimisation
    try:
        source = obj.content_type.get_object_for_this_type(id=obj.model_id)
    except:
        return None
    return source.get_absolute_url()


@register.filter
def dr_or_cr(val):
    if val < 0:
        return str(val * -1) + ' (Cr)'
    else:
        return str(val) + ' (Dr)'


@register.filter
def linkify(obj):
    return mark_safe('<a href="' + obj.get_absolute_url() + '">' + str(obj) + '</a>')


@register.filter
def remove_account(transactions, account):
    return [transaction for transaction in transactions if
            transaction.account.id != account.id]


@register.filter
def get_particulars(entry, account):
    lst = []
    source = entry.content_type.get_object_for_this_type(id=entry.object_id)
    for row in source.journal_voucher.rows.all():
        if row.account is not None and not row.account == account:
            lst.append('<a href="' + '/ledger/' + str(row.account.id) + '/#' + str(entry.id) + '">' + str(
                row.account) + '</a>')
    return ', '.join(lst)


@register.tag()
def ifusergroup(parser, token):
    """ Check to see if the currently logged in user belongs to one or more groups
    Requires the Django authentication contrib app and middleware.

    Usage: {% ifusergroup Admins %} ... {% endifusergroup %}, or
           {% ifusergroup Admins Clients Programmers Managers %} ... {% else %} ... {% endifusergroup %}

    """
    try:
        tokensp = token.split_contents()
        groups = []
        groups += tokensp[1:]
    except ValueError:
        raise template.TemplateSyntaxError("Tag 'ifusergroup' requires at least 1 argument.")

    nodelist_true = parser.parse(('else', 'endifusergroup'))
    token = parser.next_token()

    if token.contents == 'else':
        nodelist_false = parser.parse(('endifusergroup',))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()

    return GroupCheckNode(groups, nodelist_true, nodelist_false)


class GroupCheckNode(template.Node):
    def __init__(self, groups, nodelist_true, nodelist_false):
        self.groups = groups
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        user = resolve_variable('user', context)
        groups = resolve_variable('request.groups', context)

        if not user.is_authenticated():
            return self.nodelist_false.render(context)

        allowed = False
        for checkgroup in self.groups:

            if checkgroup.startswith('"') and checkgroup.endswith('"'):
                checkgroup = checkgroup[1:-1]

            if checkgroup.startswith("'") and checkgroup.endswith("'"):
                checkgroup = checkgroup[1:-1]

            try:
                group = Group.objects.get(name=checkgroup)
            except Group.DoesNotExist:
                break

            if group in groups:
                allowed = True
                break

        if allowed:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


def get_fieldset(parser, token):
    try:
        name, fields, as_, variable_name, from_, form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('bad arguments for %r' % token.split_contents()[0])

    return FieldSetNode(fields.split(','), variable_name, form)


get_fieldset = register.tag(get_fieldset)


class FieldSetNode(template.Node):
    def __init__(self, fields, variable_name, form_variable):
        self.fields = fields
        self.variable_name = variable_name
        self.form_variable = form_variable

    def render(self, context):
        form = template.Variable(self.form_variable).resolve(context)
        new_form = copy.copy(form)
        new_form.fields = SortedDict([(key, value) for key, value in form.fields.items() if key in self.fields])

        context[self.variable_name] = new_form

        return u''