""" Intercom app template tags module. """
from django.conf import settings
from django import template
from intercom.dialplan import outbound_dialstring
from intercom.models import Line
from verto.models import Client


register = template.Library()


@register.simple_tag
def get_extension(caller, extension):
    """ Return the extension for the bridge template. """
    if isinstance(caller, Client):
        return caller.channel.channel_id
    return extension.extension_number


@register.simple_tag
def get_dialstring(caller, bridge):
    """ Return the dialstring for the bridge template. """
    dialstrings = []

    # Append Lines to the array.
    tpl = '${sofia_contact(%s@%s)}'
    for line in bridge.line_set.all():
        if line != caller:
            dialstrings.append(tpl % (line.username, settings.PBX_HOSTNAME))

    # Append OutsideLines to the array.
    cid = None
    for outside_line in bridge.outsideline_set.all():
        if isinstance(caller, Line) and caller.outbound_caller_id:
            cid = caller.outbound_caller_id
        if not cid:
            cid = outside_line.default_caller_id
        dialstrings.append(
            outbound_dialstring(
                outside_line.phone_number, cid.name, cid.phone_number
            )
        )

    # Return the complete dialstring.
    return ':_:'.join(dialstrings)
