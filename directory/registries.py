""" Directory registries module. """
import logging


class DirectoryHandler:
    """ Directory handler abstract class. Apps that handle directory
    requests add custom handlers in the app's directory module. """
    # pylint: disable=too-few-public-methods

    logger = logging.getLogger('django.server')

    def process(self, request):
        """ Process request and raise django.http.Http404 or ValueError
        if request POST can't be processed, or return a tuple of template
        and context if it can. """
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
