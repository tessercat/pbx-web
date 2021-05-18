""" Gateway app config module. """
from django.apps import AppConfig


gateway_settings = {}


class GatewayConfig(AppConfig):
    """ Gateway app config. """
    name = 'gateway'

    def ready(self):
        """ Config on app ready. """
        # pylint: disable=import-outside-toplevel
        import logging
        import sys
        from gateway.models import GatewayAction

        logger = logging.getLogger('django.server')

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

        # Configure action_names.
        action_names = []
        for subclass in GatewayAction.__subclasses__():
            action_names.append(subclass._meta.model_name)
        gateway_settings['action_names'] = action_names
        for name in action_names:
            logger.info('%s %s', self.name, name)
