""" Directory registries module. """
import logging
from fsapi.registries import Handler


class DirectoryHandler(Handler):
    """ Directory handler abstract class. """
    # pylint: disable=too-few-public-methods

    def process(self, request):
        """ Return a tuple of template and context. """
        raise NotImplementedError


class _HandlerRegistry:
    """ Directory request handler registry. """
    # pylint: disable=too-few-public-methods

    _registry = []
    registry = _registry


# settings.DIRECTORY_HANDLERS
directory_handler_registry = _HandlerRegistry()


def register_directory_handler(handler):
    """ Add a directory handler to the registry."""
    directory_handler_registry.registry.append(handler)
    logging.getLogger('django.server').info(
        'Registered directory %s', handler.__class__.__name__
    )
