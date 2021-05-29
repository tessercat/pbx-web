""" Intercom app outbound template tags module. """
from django import template
from intercom.dialplan import outbound_dialstring
from intercom.models import Line


register = template.Library()


@register.simple_tag
def get_dialstring(caller, extension, dest_number):
    """ Return an outbound dialstring. """
    cid = None
    if isinstance(caller, Line) and caller.outbound_caller_id:
        cid = caller.outbound_caller_id
    if not cid:
        cid = extension.default_caller_id
    return outbound_dialstring(dest_number, cid.name, cid.phone_number)
