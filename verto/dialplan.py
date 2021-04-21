""" Verto app dialplan request handler module. """
from uuid import UUID
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from verto.models import Client
from dialplan.registries import DialplanHandler, register_dialplan_handler


class VertoDialplanHandler(DialplanHandler):
    """ Verto module dialplan request handler. """
    # pylint: disable=too-few-public-methods

    def process(self, request):
        """ Process verto dialplan requests. """
        try:
            UUID(request.POST['variable_user_name'], version=4)
        except ValueError as err:
            raise Http404 from err
        client = get_object_or_404(
            Client, client_id=request.POST['variable_user_name']
        )
        handler = settings.VERTO_DIALPLAN_HANDLERS.registry.get(
            client.channel.realm
        )
        if handler:
            self.logger.info('Processing %s', handler.__class__.__name__)
            return handler.process(request, client)
        raise Http404


register_dialplan_handler(VertoDialplanHandler())
