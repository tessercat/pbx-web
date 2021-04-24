""" Verto app config module. """
import sys
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class VertoConfig(AppConfig):
    """ Verto app config. """
    name = 'verto'

    def ready(self):
        """ Autodiscover registries and open ports. """
        autodiscover_modules('verto_directory')
        autodiscover_modules('verto_dialplan')
        if sys.argv[-1] == 'project.asgi:application':
            # pylint: disable=import-outside-toplevel
            from django.conf import settings
            from common import firewall

            firewall.accept(
                'udp',
                settings.STUN_PORT,
                settings.STUN_PORT,
            )
