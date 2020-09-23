""" Channels app config module. """
import sys
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from channels.handlers import verto_auth_handler_registry


class ChannelsConfig(AppConfig):
    """ Channels app config. """
    name = 'channels'

    def ready(self):
        """ Open ports when the app starts as an ASGI application. """
        autodiscover_modules(
            'channels', register_to=verto_auth_handler_registry
        )
        if sys.argv[-1] == 'project.asgi:application':
            # pylint: disable=import-outside-toplevel
            from django.conf import settings
            from firewall import api

            api.accept(
                'udp',
                settings.COTURN_LISTENING_PORT,
                settings.COTURN_LISTENING_PORT,
            )
