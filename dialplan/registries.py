""" Dialplan registries module. """
import logging
from fsapi.registries import Handler


class DialplanHandler(Handler):
    """ Dialplan handler abstract class. """
    # pylint: disable=too-few-public-methods

    def process(self, request):
        """ Process request and raise django.http.Http404 or ValueError
        if request POST can't be processed, or return a tuple of template
        and context if it can. """
        raise NotImplementedError


class _HandlerRegistry:
    """ Dialplan request handler registry. """
    # pylint: disable=too-few-public-methods

    _registry = []
    registry = _registry


# settings.DIALPLAN_HANDLERS
dialplan_handler_registry = _HandlerRegistry()


def register_dialplan_handler(handler):
    """ Add a dialplan handler to the registry."""
    dialplan_handler_registry.registry.append(handler)
    logging.getLogger('django.server').info(
        'Registered dialplan %s', handler.__class__.__name__
    )
