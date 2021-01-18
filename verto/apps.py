""" Verto app config module. """
import sys
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from verto.registries import verto_auth_handler_registry


class VertoConfig(AppConfig):
    """ Verto app config. """
    name = 'verto'

    def ready(self):
        """ Autodiscover registries and open ports. """
        autodiscover_modules(
            'verto', register_to=verto_auth_handler_registry
        )
        if sys.argv[-1] == 'project.asgi:application':
            # pylint: disable=import-outside-toplevel
            from django.conf import settings
            from common import firewall

            firewall.accept(
                'udp',
                settings.COTURN_LISTENING_PORT,
                settings.COTURN_LISTENING_PORT,
            )
