""" Common app config module. """
from django.apps import AppConfig


common_settings = {}


class CommonConfig(AppConfig):
    """ Configure the common app. """
    name = 'common'

    def ready(self):
        """ Init app on ready. """
        # pylint: disable=import-outside-toplevel
        from fnmatch import fnmatch
        import logging
        import os
        import sys
        from django.conf import settings
        from django.utils.module_loading import autodiscover_modules

        logger = logging.getLogger('django.server')

        # Autodiscover protected paths configuration.
        autodiscover_modules('protected_paths')

        # Configure CSS file.
        static_dir = os.path.join(
            settings.BASE_DIR, self.name, 'static', self.name
        )
        css_pattern = 'common.?????.css'
        for filename in os.listdir(os.path.join(static_dir, 'css')):
            if fnmatch(filename, css_pattern):
                common_settings['css'] = filename
                break
        logger.info('%s css %s', self.name, common_settings.get('css'))

        # Open RTP ports.
        if sys.argv[-1] == 'project.asgi:application':
            from common import firewall

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
