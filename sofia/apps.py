""" Sofia app config module. """
import sys
from django.apps import AppConfig


class SofiaConfig(AppConfig):
    """ Sofia app config. """
    name = 'sofia'

    def ready(self):
        """ Config on app ready. """

        # Open ports
        if sys.argv[-1] == 'project.asgi:application':
            # pylint: disable=import-outside-toplevel
            from common import firewall
            from sofia.models import IntercomProfile
            for intercom in IntercomProfile.objects.all():
                firewall.accept(
                    'tcp',
                    intercom.port,
                    intercom.port,
                )
            # Add gateway ports.
