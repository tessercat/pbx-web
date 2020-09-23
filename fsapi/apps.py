""" FsAPI app config module. """
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from fsapi.handlers import fsapi_request_handler_registry


class FsapiConfig(AppConfig):
    """ FsApi app config. """
    name = 'fsapi'

    def ready(self):
        """ Import handler modules on app ready. """
        autodiscover_modules(
            'fsapi', register_to=fsapi_request_handler_registry
        )
