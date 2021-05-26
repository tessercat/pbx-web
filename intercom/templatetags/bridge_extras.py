""" Intercom app template tags module. """
import logging
from django import template
from intercom.models import outbound_dialstring


register = template.Library()


@register.simple_tag
def get_dialstring(calling_line, bridge):
    """ Return the dialstring for the bridge template. """
    dialstrings = []

    # Append Lines to the array.
    logger = logging.getLogger('django.server')
    for line in bridge.line_set.all():
        logger.info(line)

    # Append OutsideLines to the array.
    for line in bridge.outsideline_set.all():
        if calling_line.outbound_caller_id:
            caller_id = calling_line.outbound_caller_id
        else:
            caller_id = line.default_caller_id
        dialstrings.append(outbound_dialstring(line.phone_number, caller_id))

    # Return the complete dialstring.
    return ':_:'.join(dialstrings)