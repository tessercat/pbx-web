""" Sofia app config module. """
from django.apps import AppConfig


class SofiaConfig(AppConfig):
    """ Sofia app config. """
    name = 'sofia'

    def ready(self):
        """ Config on app ready. """
        # pylint: disable=import-outside-toplevel
        import sys

        # Open ports.
        if sys.argv[-1] == 'project.asgi:application':
            import logging
            from common import firewall
            from sofia.models import Intercom, Gateway, AclAddress

            logger = logging.getLogger('django.server')
            for intercom in Intercom.objects.all():
                firewall.accept(
                    'tcp',
                    intercom.port,
                    intercom.port,
                )
                logger.info(
                    '%s opened tcp %s',
                    self.name, intercom.port
                )
            for gateway in Gateway.objects.all():
                for acl_addr in AclAddress.objects.filter(gateway=gateway):
                    firewall.accept(
                        'tcp',
                        gateway.port,
                        gateway.port,
                        acl_addr.address
                    )
                    logger.info(
                        '%s opened tcp %s to %s',
                        self.name, gateway.port, acl_addr.address
                    )
