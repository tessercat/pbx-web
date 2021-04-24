""" Verto app dialplan request handler module. """
from uuid import UUID
from django.http import Http404
from django.shortcuts import get_object_or_404
from dialplan.registries import DialplanHandler, register_dialplan_handler
from verto.models import Channel, Client
from verto.registries import verto_dialplan_handler_registry


class VertoDialplanHandler(DialplanHandler):
    """ Verto module dialplan request handler. """
    # pylint: disable=too-few-public-methods

    def process(self, request):
        """ Process verto dialplan requests. """
        try:
            UUID(request.POST['variable_user_name'], version=4)
        except (KeyError, ValueError) as err:
            raise Http404 from err
        client = get_object_or_404(
            Client, client_id=request.POST['variable_user_name']
        )
        try:
            application = client.channel.application
        except Channel.DoesNotExist as err:
            raise Http404 from err
        handler = verto_dialplan_handler_registry.get(
            application.__class__.__name__
        )
        if handler:
            self.logger.info('Processing %s', handler.__class__.__name__)
            return handler.process(request, client)
        raise Http404


register_dialplan_handler('verto', VertoDialplanHandler())
