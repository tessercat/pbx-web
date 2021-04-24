""" Verto registries module. """
import logging
from fsapi.registries import Handler


verto_directory_handler_registry = {}


class VertoDirectoryHandler(Handler):
    """ Verto directory handler abstract class. """
    # pylint: disable=too-few-public-methods

    def process(self, request, client):
        """ Return a tuple of template and context. """
        raise NotImplementedError


def register_verto_directory_handler(realm, handler):
    """ Add a verto auth handler to the global handler registry."""
    verto_directory_handler_registry[realm] = handler
    logging.getLogger('django.server').info(
        'Registered verto directory handler %s', handler.__class__.__name__
    )


verto_dialplan_handler_registry = {}


class VertoDialplanHandler(Handler):
    """ Verto dialplan handler abstract class. """
    # pylint: disable=too-few-public-methods

    def process(self, request, client):
        """ Return a tuple of template and context. """
        raise NotImplementedError


def register_verto_dialplan_handler(realm, handler):
    """ Add a verto auth handler to the global handler registry."""
    verto_dialplan_handler_registry[realm] = handler
    logging.getLogger('django.server').info(
        'Registered verto dialplan handler %s', handler.__class__.__name__
    )
