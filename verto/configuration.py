""" Verto app config request handler module. """
from django.conf import settings
from configuration.registries import (
    ConfigurationHandler,
    register_configuration_handler
)


class VertoConfigHandler(ConfigurationHandler):
    """ Verto config request handler. """

    def process(self, request):
        """ Return template and context. """
        template = 'verto/verto.conf.xml'
        context = {
            'verto_port': settings.VERTO_PORT,
        }
        return template, context


register_configuration_handler('verto.conf', VertoConfigHandler())
