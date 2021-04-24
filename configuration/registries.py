""" Configuration registries module. """
import logging
from fsapi.registries import Handler


configuration_handler_registry = {}


class ConfigurationHandler(Handler):
    """ Configuration handler abstract class. """
    # pylint: disable=too-few-public-methods

    def process(self, request):
        """ Return a tuple of template and context. """
        raise NotImplementedError


def register_configuration_handler(key_value, handler):
    """ Add a configuration handler to the registry."""
    configuration_handler_registry[key_value] = handler
    logging.getLogger('django.server').info(
        'Registered configuration handler %s', handler.__class__.__name__
    )
