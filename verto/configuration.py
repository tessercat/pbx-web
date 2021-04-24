""" Verto app config request handler module. """
from django.conf import settings
from configuration.registries import (
    ConfigurationHandler,
    register_configuration_handler
)


class VertoProfileHandler(ConfigurationHandler):
    """ Verto profile config request handler. """
    # pylint: disable=too-few-public-methods

    def process(self, request):
        """ Process verto profile configuration requests. """
        # pylint: disable=no-self-use
        template = 'verto/verto.conf.xml'
        context = {
            'debug_level': 10,
            'verto_port': settings.VERTO_PORT,
        }
        return template, context


register_configuration_handler('verto.conf', VertoProfileHandler())
