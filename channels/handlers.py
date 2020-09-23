""" Channels app verto auth request handler module. """
import logging


class AuthHandler:
    """ Verto auth handler abstract class. Apps that handle verto auth
    requests add custom AuthHandlers in the app's channels module. """
    # pylint: disable=too-few-public-methods

    logger = logging.getLogger('django.server')

    def process(self, request, session):
        """ Process request and session and raise django.http.Http404
        or ValueError if request POST and session data can't be processed,
        or return a tuple of template and context if it can. """
        raise NotImplementedError


class AuthHandlerRegistry:
    """ Verto auth handler registry. """
    # pylint: disable=too-few-public-methods

    _registry = {}
    registry = _registry


verto_auth_handler_registry = AuthHandlerRegistry()


def register_handler(realm, handler):
    """ Add a verto auth handler to the global handler registry."""
    verto_auth_handler_registry.registry[realm] = handler
    logging.getLogger('django.server').info(
        'Registered %s', handler.__class__.__name__
    )
