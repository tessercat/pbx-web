""" Directory registries module. """
import logging
from fsapi.registries import Handler


directory_handler_registry = {}


class DirectoryHandler(Handler):
    """ Directory handler abstract class. """
    # pylint: disable=too-few-public-methods

    def process(self, request):
        """ Return a tuple of template and context. """
        raise NotImplementedError


def register_directory_handler(domain, handler):
    """ Add a directory handler to the registry."""
    directory_handler_registry[domain] = handler
    logging.getLogger('django.server').info(
        'Registered directory handler %s', handler.__class__.__name__
    )
