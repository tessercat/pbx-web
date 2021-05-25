""" Intercom app template tags module. """
import logging
from django import template
from sofia.models import Gateway


register = template.Library()


@register.simple_tag
def get_dialstring(calling_line, bridge):
    """ Return the dialstring for the bridge template. """
    lines = []

    # Append Lines to the dialsting array.
    logger = logging.getLogger('django.server')
    for line in bridge.line_set.all():
        logger.info(line)

    # Append OutsideLines to the dialstring array.
    outside_lines = bridge.outsideline_set.all()
    if outside_lines:
        dialstring = '[%s,%s]sofia/gateway/%s/%s'
        cid_name = 'origination_caller_id_name=%s'
        cid_number = 'origination_caller_id_number=%s'
        # Cache gateways somehow. They aren't dynamic.
        gateway = Gateway.objects.order_by('priority')[0]
        for outside_line in outside_lines:
            if calling_line.outbound_caller_id:
                caller_id = calling_line.outbound_caller_id
            else:
                caller_id = outside_line.default_caller_id
            lines.append(
                dialstring % (
                    cid_name % caller_id.name,
                    cid_number % caller_id.phone_number,
                    gateway.domain,
                    outside_line.phone_number
                )
            )

    # Return the joined dialstring.
    return ':_:'.join(lines)
