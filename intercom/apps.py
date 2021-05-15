""" Intercom app config module. """
from django.apps import AppConfig


class IntercomConfig(AppConfig):
    """ Intercom app config. """
    name = 'intercom'

    def ready(self):
        """ Config on app ready. """
        # pylint: disable=import-outside-toplevel
        import sys

        # Open ports
        if sys.argv[-1] == 'project.asgi:application':
            from common import firewall
            from intercom.models import Intercom

            for intercom in Intercom.objects.all():
                firewall.accept(
                    'tcp',
                    intercom.port,
                    intercom.port,
                )
