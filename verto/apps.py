""" Verto app config module. """
from django.apps import AppConfig


class VertoConfig(AppConfig):
    """ Verto app config. """
    name = 'verto'

    def ready(self):
        """ Configure verto app. """
        # pylint: disable=import-outside-toplevel
        import sys

        if sys.argv[-1] == 'project.asgi:application':
            import logging
            from django.conf import settings
            from common import firewall

            firewall.accept(
                'udp',
                settings.PORTS['stun'],
                settings.PORTS['stun'],
            )
            logging.getLogger('django.server').info(
                '%s opened udp %s',
                self.name, settings.PORTS['stun']
            )
