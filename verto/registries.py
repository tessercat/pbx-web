""" Verto auth registries module. """
import logging


class AuthHandler:
    """ Verto auth handler abstract class. Apps that handle verto auth
    requests add custom AuthHandlers in the app's verto module. """
    # pylint: disable=too-few-public-methods

    logger = logging.getLogger('django.server')

    def process(self, request, client):
        """ Process request and client and raise django.http.Http404
        or ValueError if request POST and client data can't be processed,
        or return a tuple of template and context if it can. """
        raise NotImplementedError


class _HandlerRegistry:
    """ Verto auth handler registry. """
    # pylint: disable=too-few-public-methods

    _registry = {}
    registry = _registry


# settings.VERTO_AUTH_HANDLERS
verto_auth_handler_registry = _HandlerRegistry()


def register_verto_auth_handler(realm, handler):
    """ Add a verto auth handler to the global handler registry."""
    verto_auth_handler_registry.registry[realm] = handler
    logging.getLogger('django.server').info(
        'Registered verto %s', handler.__class__.__name__
    )
