""" Gateway app dialplan request handler module. """
from django.db.utils import OperationalError
from django.http import Http404
from django.shortcuts import get_object_or_404
from dialplan.registries import DialplanHandler, register_dialplan_handler
from gateway.apps import gateway_settings
from gateway.models import Gateway, DidNumber


class GatewayDialplanHandler(DialplanHandler):
    """ Gateway dialplan request handler. """

    def get_dialplan(self, request, context):
        """ Return template/context. """

        # Get a DidNumber's Extension.
        number = request.POST.get('Caller-Destination-Number')
        if not number:
            raise Http404
        did_number = get_object_or_404(
            DidNumber,
            number=number,
            gateway__domain=context
        )
        if not hasattr(did_number, 'extension'):
            raise Http404
        extension = did_number.extension

        # Get the Extension's action.
        action = None
        if hasattr(extension, 'gatewayaction'):
            for name in gateway_settings['action_names']:
                if hasattr(extension.gatewayaction, name):
                    action = getattr(extension.gatewayaction, name)
                    break
        if not action:
            raise Http404

        # Return the template/context.
        template = action.template
        context = {
            'context': context,
            'action': action,
        }
        self.log_rendered(request, template, context)
        return template, context


# These fail to load until tables exist.
try:
    for _gateway in Gateway.objects.all():
        register_dialplan_handler(_gateway.domain, GatewayDialplanHandler())
except OperationalError:
    pass
