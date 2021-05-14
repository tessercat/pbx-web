""" Gateway app config module. """
from django.apps import AppConfig


class GatewayConfig(AppConfig):
    """ Gateway app config. """
    name = 'gateway'

    def ready(self):
        """ Config on app ready. """
        # pylint: disable=import-outside-toplevel
        import sys

        # Open ports
        if sys.argv[-1] == 'project.asgi:application':
            from common import firewall
            from gateway.models import Gateway, AclAddress

            for gateway in Gateway.objects.all():
                for acl_addr in AclAddress.objects.filter(gateway=gateway):
                    firewall.accept(
                        'tcp',
                        gateway.port,
                        gateway.port,
                        acl_addr.address
                    )
