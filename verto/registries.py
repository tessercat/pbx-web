""" Verto request handler registries module. """
import logging


class VertoDirectoryHandler:
    """ Verto directory handler abstract class. """
    # pylint: disable=too-few-public-methods

    logger = logging.getLogger('django.server')

    def process(self, request, client):
        """ Process request and client and raise django.http.Http404
        or ValueError if request POST and client data can't be processed,
        or return a tuple of template and context if it can. """
        raise NotImplementedError


class _DirectoryHandlerRegistry:
    """ Verto directory handler registry. """
    # pylint: disable=too-few-public-methods

    _registry = {}
    registry = _registry


# settings.VERTO_DIRECTORY_HANDLERS
verto_directory_handler_registry = _DirectoryHandlerRegistry()


def register_verto_directory_handler(realm, handler):
    """ Add a verto auth handler to the global handler registry."""
    verto_directory_handler_registry.registry[realm] = handler
    logging.getLogger('django.server').info(
        'Registered verto %s', handler.__class__.__name__
    )


class VertoDialplanHandler:
    """ Verto dialplan handler abstract class. """
    # pylint: disable=too-few-public-methods

    logger = logging.getLogger('django.server')

    def process(self, request, client):
        """ Process request and client and raise django.http.Http404
        or ValueError if request POST and client data can't be processed,
        or return a tuple of template and context if it can. """
        raise NotImplementedError


class _DialplanHandlerRegistry:
    """ Verto dialplan handler registry. """
    # pylint: disable=too-few-public-methods

    _registry = {}
    registry = _registry


# settings.VERTO_DIALPLAN_HANDLERS
verto_dialplan_handler_registry = _DialplanHandlerRegistry()


def register_verto_dialplan_handler(realm, handler):
    """ Add a verto auth handler to the global handler registry."""
    verto_dialplan_handler_registry.registry[realm] = handler
    logging.getLogger('django.server').info(
        'Registered verto %s', handler.__class__.__name__
    )
