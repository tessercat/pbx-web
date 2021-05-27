""" Intercom app config module. """
from django.apps import AppConfig


intercom_settings = {}


# pylint: disable=import-outside-toplevel
class IntercomConfig(AppConfig):
    """ Intercom app config. """
    name = 'intercom'

    def config_action_names(self):
        """ Add action_names to settings. """
        # pylint: disable=no-self-use
        self.config_static()
        from intercom.models import Action

        action_names = []
        for subclass in Action.__subclasses__():
            action_names.append(subclass._meta.model_name)
        intercom_settings['action_names'] = action_names

    def config_dialplan_handlers(self):
        """ Configure dialplan handlers. """
        # pylint: disable=no-self-use
        from dialplan.fsapi import register_dialplan_handler
        from intercom.dialplan import (
            ClientCallHandler,
            LineCallHandler,
            GatewayCallHandler
        )
        from sofia.models import Intercom, Gateway

        register_dialplan_handler('verto', ClientCallHandler())
        for intercom in Intercom.objects.all():
            register_dialplan_handler(intercom.domain, LineCallHandler())
        for gateway in Gateway.objects.all():
            register_dialplan_handler(gateway.domain, GatewayCallHandler())

    def config_directory_handlers(self):
        """ Configure directory handlers. """
        # pylint: disable=no-self-use
        from directory.fsapi import register_directory_handler
        from intercom.models import Intercom
        from intercom.directory import LineAuthHandler, ClientAuthHandler

        for intercom in Intercom.objects.all():
            register_directory_handler(intercom.domain, LineAuthHandler())
        register_directory_handler('verto', ClientAuthHandler())

    def config_gateways(self):
        """ Add gateways to settings. """
        # pylint: disable=no-self-use
        from sofia.models import Gateway

        intercom_settings['gateways'] = list(
            Gateway.objects.order_by('priority')
        )

    def config_static(self):
        """ Add static files to settings. """
        from fnmatch import fnmatch
        import os
        from django.conf import settings

        root = os.path.join(settings.BASE_DIR, self.name, 'static', self.name)

        # Configure client CSS file.
        for filename in os.listdir(os.path.join(root, 'css')):
            if fnmatch(filename, 'client.?????.css'):
                intercom_settings['css'] = filename
                break

        # Configure client JS files.
        for filename in os.listdir(os.path.join(root, 'js')):
            if fnmatch(filename, 'adapter.?????.js'):
                intercom_settings['adapter'] = filename
                continue
            if fnmatch(filename, 'client.?????.js'):
                intercom_settings['client'] = filename
                continue

    def ready(self):
        """ Config on app ready. """
        import logging
        from django.db.utils import OperationalError

        self.config_action_names()
        self.config_static()
        try:
            self.config_gateways()
            self.config_dialplan_handlers()
            self.config_directory_handlers()
        except OperationalError:
            pass  # These fail when tables don't exist.

        # Log settings.
        logger = logging.getLogger('django.server')
        for key, value in intercom_settings.items():
            logger.info('%s %s %s', self.name, key, value)
