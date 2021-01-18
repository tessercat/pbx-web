""" Fsapi app config module. """
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from fsapi.registries import fsapi_request_handler_registry


class FsapiConfig(AppConfig):
    """ Fsapi app config. """
    name = 'fsapi'

    def ready(self):
        """ Autodiscover registries. """
        autodiscover_modules(
            'fsapi', register_to=fsapi_request_handler_registry
        )
