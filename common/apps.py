""" Common app config module. """
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


common_settings = {}


class CommonConfig(AppConfig):
    """ Configure the common app. """
    name = 'common'

    def config_static(self):
        """ Add static file settings. """
        import os
        from fnmatch import fnmatch
        from django.conf import settings

        root = os.path.join(settings.BASE_DIR, self.name, 'static', self.name)
        css_pattern = 'common.?????.css'
        for filename in os.listdir(os.path.join(root, 'css')):
            if fnmatch(filename, css_pattern):
                common_settings['css'] = filename
                break

    def ready(self):
        """ Init app on ready. """
        # pylint: disable=import-outside-toplevel
        import logging
        import sys

        autodiscover_modules('protected_paths')
        self.config_static()
        logger = logging.getLogger('django.server')
        for key, value in common_settings.items():
            logger.info('%s %s %s', self.name, key, value)

        # Open RTP ports.
        if sys.argv[-1] == 'project.asgi:application':
            from common import firewall
            from django.conf import settings

            firewall.accept(
                'udp',
                settings.PORTS['rtp_start'],
                settings.PORTS['rtp_end']
            )
            logger.info(
                '%s opened udp %s-%s',
                self.name,
                settings.PORTS['rtp_start'],
                settings.PORTS['rtp_end']
            )
