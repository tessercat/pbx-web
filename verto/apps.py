""" Verto app config module. """
import sys
from django.apps import AppConfig


class VertoConfig(AppConfig):
    """ Verto app config. """
    name = 'verto'

    def ready(self):
        """ Configure verto app. """
        if sys.argv[-1] == 'project.asgi:application':
            # pylint: disable=import-outside-toplevel
            from django.conf import settings
            from common import firewall

            firewall.accept(
                'udp',
                settings.STUN_PORT,
                settings.STUN_PORT,
            )
