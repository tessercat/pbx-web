""" Conference app config module. """
from fnmatch import fnmatch
import os
from django.apps import AppConfig


class ConferenceConfig(AppConfig):
    """ Conference app config class. """
    name = 'conference'

    def ready(self):
        """ Configure app file settings. """
        # pylint: disable=import-outside-toplevel
        import logging
        from django.conf import settings

        # conference.css
        pattern = 'conference.?????.css'
        app_dir = os.path.join(
            settings.BASE_DIR, 'conference', 'static', 'conference', 'css'
        )
        logging.getLogger('django.server').info('Configuring CONFERENCE_CSS')
        for filename in os.listdir(app_dir):
            if fnmatch(filename, pattern):
                logging.getLogger('django.server').info(
                    'Configured CONFERENCE_CSS %s', filename
                )
                settings.CONFERENCE_CSS = filename

        # client.js and adapter.js
        app_dir = os.path.join(
            settings.BASE_DIR, 'conference', 'static', 'conference', 'js'
        )
        client_pattern = 'client.?????.js'
        adapter_pattern = 'adapter.?????.js'
        logging.getLogger('django.server').info(
            'Configuring CONFERENCE_CLIENT_JS and CONFERENCE_ADAPTER_JS'
        )
        for filename in os.listdir(app_dir):
            if fnmatch(filename, client_pattern):
                logging.getLogger('django.server').info(
                    'Configured CONFERENCE_CLIENT_JS %s', filename
                )
                settings.CONFERENCE_CLIENT_JS = filename
            if fnmatch(filename, adapter_pattern):
                logging.getLogger('django.server').info(
                    'Configured CONFERENCE_ADAPTER_JS %s', filename
                )
                settings.CONFERENCE_ADAPTER_JS = filename
