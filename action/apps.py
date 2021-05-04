""" Action app config module. """
import logging
from fnmatch import fnmatch
import os
from django.apps import AppConfig
from django.db.models import signals


action_settings = {}


class ActionConfig(AppConfig):
    """ Action app config. """
    name = 'action'

    def ready(self):
        """ Init app on ready. """
        # pylint: disable=import-outside-toplevel
        from django.conf import settings
        from action.models import (
            Action, post_save_handler, post_delete_handler
        )

        # Configure static files.
        logger = logging.getLogger('django.server')
        static_dir = os.path.join(
            settings.BASE_DIR, self.name, 'static', self.name
        )

        # Configure CSS file.
        css_pattern = 'client.?????.css'
        for filename in os.listdir(os.path.join(static_dir, 'css')):
            if fnmatch(filename, css_pattern):
                action_settings['css'] = filename
                break
        logger.info('%s css %s', self.name, action_settings.get('css'))

        # Configure JS files.
        js_pattern = 'client.?????.js'
        adapter_pattern = 'adapter.?????.js'
        for filename in os.listdir(os.path.join(static_dir, 'js')):
            if fnmatch(filename, adapter_pattern):
                action_settings['adapter'] = filename
                continue
            if fnmatch(filename, js_pattern):
                action_settings['client'] = filename
                continue
        logger.info('%s adapter %s', self.name, action_settings.get('adapter'))
        logger.info('%s client %s', self.name, action_settings.get('client'))

        # Configure action_names.
        action_names = []
        for action in Action.__subclasses__():
            signals.post_save.connect(post_save_handler, action)
            signals.post_delete.connect(post_delete_handler, action)
            action_names.append(action._meta.model_name)
        action_settings['action_names'] = action_names
        logger.info('%s subclasses %s', self.name, ' '.join(action_names))
