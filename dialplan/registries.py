""" Dialplan registries module. """
import logging
from fsapi.registries import Handler


dialplan_handler_registry = {}


class DialplanHandler(Handler):
    """ Dialplan handler abstract class. """
    # pylint: disable=too-few-public-methods

    def process(self, request):
        """ Return a tuple of template and context. """
        raise NotImplementedError


def register_dialplan_handler(context, handler):
    """ Add a dialplan handler to the registry."""
    dialplan_handler_registry[context] = handler
    logging.getLogger('django.server').info(
        'Registered dialplan handler %s', handler.__class__.__name__
    )
