""" Extension app config module. """
from django.apps import AppConfig


extension_settings = {}


class ExtensionConfig(AppConfig):
    """ Extension app config. """
    name = 'extension'

    def ready(self):
        """ Init app on ready. """
        # pylint: disable=import-outside-toplevel
        from fnmatch import fnmatch
        import logging
        import os
        from django.conf import settings
        from django.db.models import signals
        from extension.models import (
            Action, post_save_handler, post_delete_handler
        )

        # Configure static files.
        logger = logging.getLogger('django.server')
        static_dir = os.path.join(
            settings.BASE_DIR, self.name, 'static', self.name
        )

        # Configure CSS file.
        for filename in os.listdir(os.path.join(static_dir, 'css')):
            if fnmatch(filename, 'client.?????.css'):
                extension_settings['css'] = filename
                break
        logger.info('%s css %s', self.name, extension_settings.get('css'))

        # Configure JS files.
        for filename in os.listdir(os.path.join(static_dir, 'js')):
            if fnmatch(filename, 'adapter.?????.js'):
                extension_settings['adapter'] = filename
                continue
            if fnmatch(filename, 'client.?????.js'):
                extension_settings['client'] = filename
                continue
        logger.info(
            '%s adapter %s', self.name, extension_settings.get('adapter')
        )
        logger.info(
            '%s client %s', self.name, extension_settings.get('client')
        )

        # Configure action_names.
        action_names = []
        for extension in Action.__subclasses__():
            signals.post_save.connect(post_save_handler, extension)
            signals.post_delete.connect(post_delete_handler, extension)
            action_names.append(extension._meta.model_name)
        extension_settings['action_names'] = action_names
        logging.getLogger('django.server').info(
            '%s subclasses %s', self.name, ' '.join(action_names)
        )
