""" Fsapi app config module. """
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class FsapiConfig(AppConfig):
    """ Fsapi app config. """
    name = 'fsapi'

    def ready(self):
        """ Autodiscover registries. """
        autodiscover_modules('fsapi')
