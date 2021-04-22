""" Verto registries module. """
import logging
from fsapi.registries import Handler


class VertoDirectoryHandler(Handler):
    """ Verto directory handler abstract class. """
    # pylint: disable=too-few-public-methods

    def process(self, request, client):
        """ Return a tuple of template and context. """
        raise NotImplementedError


class _DirectoryHandlerRegistry:
    """ Verto directory handler registry. """
    # pylint: disable=too-few-public-methods

    _registry = {}
    registry = _registry


verto_directory_handler_registry = _DirectoryHandlerRegistry()


def register_verto_directory_handler(realm, handler):
    """ Add a verto auth handler to the global handler registry."""
    verto_directory_handler_registry.registry[realm] = handler
    logging.getLogger('django.server').info(
        'Registered verto %s', handler.__class__.__name__
    )


class VertoDialplanHandler(Handler):
    """ Verto dialplan handler abstract class. """
    # pylint: disable=too-few-public-methods

    def process(self, request, client):
        """ Return a tuple of template and context. """
        raise NotImplementedError


class _DialplanHandlerRegistry:
    """ Verto dialplan handler registry. """
    # pylint: disable=too-few-public-methods

    _registry = {}
    registry = _registry


verto_dialplan_handler_registry = _DialplanHandlerRegistry()


def register_verto_dialplan_handler(realm, handler):
    """ Add a verto auth handler to the global handler registry."""
    verto_dialplan_handler_registry.registry[realm] = handler
    logging.getLogger('django.server').info(
        'Registered verto %s', handler.__class__.__name__
    )
