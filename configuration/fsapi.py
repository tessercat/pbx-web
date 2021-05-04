""" Configuration request handler module. """
from django.http import Http404
from fsapi.registries import FsapiHandler, register_fsapi_handler
from configuration.registries import configuration_handler_registry


class ConfigurationHandler(FsapiHandler):
    """ Handler for all configuration requests. """

    def __init__(self):
        super().__init__(
            section='configuration',
        )

    def process(self, request):
        """ Process configuration request key_value handler. """
        key_value = request.POST.get('key_value')
        if not key_value:
            self.logger.info('No configuration key found')
            self.logger.info(request.POST.dict())
            raise Http404
        handler = configuration_handler_registry.get(key_value)
        if not handler:
            self.logger.info('No configuration handler for %s', key_value)
            raise Http404
        return handler.process(request)


register_fsapi_handler(ConfigurationHandler())
