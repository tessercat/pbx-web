""" Directory request handler module. """
from django.conf import settings
from django.http import Http404
from fsapi.registries import FsapiHandler, register_fsapi_handler


class DirectoryFsapiHandler(FsapiHandler):
    """ Handler for all directory requests. Pass requests to sub-handlers. """

    def __init__(self):
        super().__init__(
            domain=settings.PBX_HOSTNAME,
            section='directory',
        )

    def process(self, request):
        """ Process registry handlers until a sub-handler doesn't raise 404
        or until there are no more handlers to try. """
        for handler in settings.DIRECTORY_HANDLERS.registry:
            self.logger.info('Processing %s', handler.__class__.__name__)
            try:
                return handler.process(request)
            except Http404:
                continue
        raise Http404


register_fsapi_handler(DirectoryFsapiHandler())
