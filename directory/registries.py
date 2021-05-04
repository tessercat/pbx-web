""" Directory registries module. """
import logging
from fsapi.registries import Handler


directory_handler_registry = {}


class DirectoryHandler(Handler):
    """ Directory handler abstract class. """

    def get_directory(self, request, domain):
        """ Return template/context. """
        raise NotImplementedError


def register_directory_handler(domain, handler):
    """ Add a directory handler to the registry."""
    directory_handler_registry[domain] = handler
    logging.getLogger('django.server').info(
        'directory %s %s', handler.__class__.__name__, domain
    )
