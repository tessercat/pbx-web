""" Verto app directory request handler module. """
from uuid import UUID
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from verto.models import Channel, Client
from directory.registries import DirectoryHandler, register_directory_handler


class VertoDirectoryHandler(DirectoryHandler):
    """ Verto module directory request handler. """
    # pylint: disable=too-few-public-methods

    def process(self, request):
        """ Process verto directory requests. """
        try:
            UUID(request.POST['user'], version=4)
        except (KeyError, ValueError) as err:
            raise Http404 from err
        client = get_object_or_404(Client, client_id=request.POST['user'])
        try:
            application = client.channel.application
        except Channel.DoesNotExist as err:
            raise Http404 from err
        handler = settings.VERTO_DIRECTORY_HANDLERS.registry.get(
            application.__class__.__name__
        )
        if handler:
            self.logger.info('Processing %s', handler.__class__.__name__)
            return handler.process(request, client)
        raise Http404


register_directory_handler(VertoDirectoryHandler())
