""" Directory request handler module. """
from django.http import Http404
from fsapi.registries import FsapiHandler, register_fsapi_handler
from directory.registries import directory_handler_registry


class DirectoryHandler(FsapiHandler):
    """ Handler for all directory requests. """

    def __init__(self):
        super().__init__(
            section='directory',
        )

    def process(self, request):
        """ Process request by directory domain. """
        domain = request.POST.get('domain')
        if not domain:
            self.logger.info('No directory domain found')
            self.logger.info(request.POST.dict())
            raise Http404
        handler = directory_handler_registry.get(domain)
        if not handler:
            self.logger.info('No directory handler for %s', domain)
            raise Http404
        return handler.get_directory(request, domain)


register_fsapi_handler(DirectoryHandler())
