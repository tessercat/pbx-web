""" Common app config module. """
from fnmatch import fnmatch
import logging
import os
import sys
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


common_settings = {}


class CommonConfig(AppConfig):
    """ Configure the common app. """
    name = 'common'

    def ready(self):
        """ Init app on ready. """
        # pylint: disable=import-outside-toplevel
        from django.conf import settings

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
        logging.getLogger('django.server').info(
            '%s css %s', self.name, common_settings.get('css')
        )

        # Open RTP ports.
        if sys.argv[-1] == 'project.asgi:application':
            from common import firewall

            firewall.accept(
                'udp',
                settings.RTP_PORT_START,
                settings.RTP_PORT_END,
            )
