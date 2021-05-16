""" Gateway app dialplan request handler module. """
from django.db.utils import OperationalError
from django.http import Http404
from django.shortcuts import get_object_or_404
from dialplan.registries import DialplanHandler, register_dialplan_handler
from gateway.models import Gateway, DidNumber


class GatewayDialplanHandler(DialplanHandler):
    """ Handle an gateway context dialplan request. """

    def get_action(self, request, context):
        """ Return an Action. """
        number = request.POST.get('Caller-Destination-Number')
        if not number:
            raise Http404
        did_number = get_object_or_404(
            DidNumber,
            number=number,
            gateway__domain=context
        )
        if hasattr(did_number, 'extension'):
            extension = did_number.extension
            if hasattr(extension, 'action'):
                return extension.action.get_action()
        raise Http404


# These fail to load until tables exist.
try:
    for _gateway in Gateway.objects.all():
        register_dialplan_handler(_gateway.domain, GatewayDialplanHandler())
except OperationalError:
    pass
