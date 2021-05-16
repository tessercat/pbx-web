""" Intercom app config module. """
from django.apps import AppConfig


intercom_settings = {}


class IntercomConfig(AppConfig):
    """ Intercom app config. """
    name = 'intercom'

    def ready(self):
        """ Config on app ready. """
        # pylint: disable=import-outside-toplevel
        from fnmatch import fnmatch
        import logging
        import os
        import sys
        from django.conf import settings

        # Open port.
        if sys.argv[-1] == 'project.asgi:application':
            from common import firewall
            from intercom.models import Intercom

            for intercom in Intercom.objects.all():
                firewall.accept(
                    'tcp',
                    intercom.port,
                    intercom.port,
                )

        # Configure static files.
        logger = logging.getLogger('django.server')
        static_dir = os.path.join(
            settings.BASE_DIR, self.name, 'static', self.name
        )

        # Configure client CSS file.
        for filename in os.listdir(os.path.join(static_dir, 'css')):
            if fnmatch(filename, 'client.?????.css'):
                intercom_settings['css'] = filename
                break
        logger.info('%s css %s', self.name, intercom_settings.get('css'))

        # Configure client JS files.
        for filename in os.listdir(os.path.join(static_dir, 'js')):
            if fnmatch(filename, 'adapter.?????.js'):
                intercom_settings['adapter'] = filename
                continue
            if fnmatch(filename, 'client.?????.js'):
                intercom_settings['client'] = filename
                continue
        logger.info(
            '%s adapter %s', self.name, intercom_settings.get('adapter')
        )
        logger.info(
            '%s client %s', self.name, intercom_settings.get('client')
        )
