from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class ConfigurationConfig(AppConfig):
    name = 'configuration'

    def ready(self):
        """ Autodiscover handlers in other modules. """
        autodiscover_modules('configuration')
