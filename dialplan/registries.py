""" Dialplan registries module. """
import logging
from fsapi.registries import Handler


dialplan_handler_registry = {}


class DialplanHandler(Handler):
    """ Dialplan handler abstract class. """

    def get_dialplan(self, request, context):
        """ Return template/context. """
        raise NotImplementedError


def register_dialplan_handler(context, handler):
    """ Add a dialplan handler to the registry."""
    dialplan_handler_registry[context] = handler
    logging.getLogger('django.server').info(
        'dialplan %s %s', handler.__class__.__name__, context
    )
