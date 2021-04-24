""" Common app config module. """
from fnmatch import fnmatch
import os
import sys
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class CommonConfig(AppConfig):
    """ Configure the common app. """
    name = 'common'

    def ready(self):
        """ Init app on ready. """
        # pylint: disable=import-outside-toplevel
        import logging
        from django.conf import settings

        # Autodiscover protected paths configuration.
        autodiscover_modules('protected_paths')

        # Configure common CSS file.
        pattern = 'common.?????.css'
        app_dir = os.path.join(
            settings.BASE_DIR, 'common', 'static', 'common', 'css'
        )
        logging.getLogger('django.server').info('Configuring COMMON_CSS')
        for filename in os.listdir(app_dir):
            if fnmatch(filename, pattern):
                settings.COMMON_CSS = filename
                logging.getLogger('django.server').info(
                    'Configured COMMON_CSS %s', filename
                )

        # Open RTP ports.
        if sys.argv[-1] == 'project.asgi:application':
            from common import firewall

            firewall.accept(
                'udp',
                settings.RTP_PORT_START,
                settings.RTP_PORT_END,
            )
