""" Gateway app dialplan request handler module. """
from django.db.utils import OperationalError
from django.http import Http404
from django.shortcuts import get_object_or_404
from dialplan.registries import register_dialplan_handler
from extension.dialplan import ExtensionHandler
from gateway.models import Gateway, DidNumber


class GatewayHandler(ExtensionHandler):
    """ Handle an gateway context dialplan request. """

    def get_extension(self, request, context):
        """ Return an Extension. """
        number = request.POST.get('Caller-Destination-Number')
        if not number:
            raise Http404
        obj = get_object_or_404(
            DidNumber,
            number=number,
            gateway__domain=context
        )
        if getattr(obj, 'extension'):
            return obj.extension.get_extension()
        raise Http404


# These fail to load until tables exist.
try:
    for _gateway in Gateway.objects.all():
        register_dialplan_handler(_gateway.domain, GatewayHandler())
except OperationalError:
    pass
