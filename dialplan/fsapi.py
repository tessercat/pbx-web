""" Dialplan request handler module. """
from django.conf import settings
from django.http import Http404
from fsapi.registries import FsapiHandler, register_fsapi_handlers


class DialplanHandler(FsapiHandler):
    """ Dialplan request handler. """

    def __init__(self):
        super().__init__(
            variable_domain_name=settings.PBX_HOSTNAME,
            section='dialplan',
        )

    def process(self, request):
        """ Process dialplan requests with handlers in the registry until
        a match is found or there are no more registered handlers. """
        for handler in settings.DIALPLAN_HANDLERS.registry:
            self.logger.info('Processing %s', handler.__class__.__name__)
            return handler.process(request)
        raise Http404


register_fsapi_handlers(
    DialplanHandler(),
)
