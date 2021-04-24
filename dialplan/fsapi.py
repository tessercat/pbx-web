""" Dialplan request handler module. """
from django.http import Http404
from fsapi.registries import FsapiHandler, register_fsapi_handler
from dialplan.registries import dialplan_handler_registry


class DialplanHandler(FsapiHandler):
    """ Handler for all dialplan requests. """

    def __init__(self):
        super().__init__(
            section='dialplan',
        )

    def process(self, request):
        """ Process request by dialplan context. """
        context = request.POST.get('Caller-Context')
        if not context:
            self.logger.info('No dialplan context found')
            self.logger.info(request.POST.dict())
            raise Http404
        handler = dialplan_handler_registry.get(context)
        if not handler:
            self.logger.info('No dialplan handler for %s', context)
            raise Http404
        self.logger.info('Processing %s', handler.__class__.__name__)
        return handler.process(request)


register_fsapi_handler(DialplanHandler())
