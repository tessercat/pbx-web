""" Gateway app dialplan request handler module. """
from django.db.utils import OperationalError
from django.http import Http404
from django.shortcuts import get_object_or_404
from dialplan.registries import DialplanHandler, register_dialplan_handler
from intercom_dialplan.models import InboundTransfer
from gateway.models import Gateway, DidNumber


class GatewayCallHandler(DialplanHandler):
    """ Gateway inbound call dialplan request handler. """

    # Handle 404 with an annotation.
    def get_dialplan(self, request, domain):
        """ Return template/context. """
        number = request.POST.get('Caller-Destination-Number')
        if not number:
            raise Http404
        did_number = get_object_or_404(
            DidNumber,
            number=number,
            gateway__domain=domain
        )
        transfer = get_object_or_404(InboundTransfer, did_number=did_number)
        template = transfer.template
        context = {
            'did_number': did_number,
            'transfer': transfer
        }
        self.log_rendered(request, template, context)
        return template, context


# These fail to load until tables exist.
try:
    for _gateway in Gateway.objects.all():
        register_dialplan_handler(_gateway.domain, GatewayCallHandler())
except OperationalError:
    pass
