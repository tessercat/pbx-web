""" Peers app config module. """
from fnmatch import fnmatch
import os
from django.apps import AppConfig


class PeersConfig(AppConfig):
    """ Peers app config class. """
    name = 'peers'

    def ready(self):
        """ Configure app file settings. """
        # pylint: disable=import-outside-toplevel
        import logging
        from django.conf import settings

        # peer.css
        pattern = 'peer.?????.css'
        app_dir = os.path.join(
            settings.BASE_DIR, 'peers', 'static', 'peers', 'css'
        )
        logging.getLogger('django.server').info('Configuring PEERS_CSS')
        for filename in os.listdir(app_dir):
            if fnmatch(filename, pattern):
                logging.getLogger('django.server').info(
                    'Configured PEERS_CSS %s', filename
                )
                settings.PEERS_CSS = filename

        # peer.js and adapter.js
        app_dir = os.path.join(
            settings.BASE_DIR, 'peers', 'static', 'peers', 'js'
        )
        peer_pattern = 'peer.?????.js'
        adapter_pattern = 'adapter.?????.js'
        logging.getLogger('django.server').info(
            'Configuring PEERS_PEER_JS and PEERS_ADAPTER_JS'
        )
        for filename in os.listdir(app_dir):
            if fnmatch(filename, peer_pattern):
                logging.getLogger('django.server').info(
                    'Configured PEERS_PEER_JS %s', filename
                )
                settings.PEERS_PEER_JS = filename
            if fnmatch(filename, adapter_pattern):
                logging.getLogger('django.server').info(
                    'Configured PEERS_ADAPTER_JS %s', filename
                )
                settings.PEERS_ADAPTER_JS = filename
