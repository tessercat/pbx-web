""" Intercom app config module. """
from django.apps import AppConfig


intercom_settings = {}


# pylint: disable=import-outside-toplevel
class IntercomConfig(AppConfig):
    """ Intercom app config. """
    name = 'intercom'

    def config_action_names(self):
        """ Add action_names to settings. """
        from intercom.models import Action

        action_names = []
        for subclass in Action.__subclasses__():
            action_names.append(subclass._meta.model_name)
        intercom_settings['action_names'] = action_names

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

        self.config_static()
        self.config_action_names()
        logger = logging.getLogger('django.server')
        for key, value in intercom_settings.items():
            logger.info('%s %s %s', self.name, key, value)
