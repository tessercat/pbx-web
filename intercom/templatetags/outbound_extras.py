""" Intercom app outbound template tags module. """
from django import template
from intercom.models import outbound_dialstring


register = template.Library()


@register.simple_tag
def get_dialstring(calling_line, extension, phone_number):
    """ Return an outbound dialstring. """
    if calling_line.outbound_caller_id:
        caller_id = calling_line.outbound_caller_id
    else:
        caller_id = extension.default_caller_id
    return outbound_dialstring(phone_number, caller_id)
