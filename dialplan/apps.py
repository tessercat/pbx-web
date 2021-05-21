""" Dialplan app config module. """
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class DialplanConfig(AppConfig):
    """ Dialplan app config. """
    name = 'dialplan'

    def ready(self):
        """ Autodiscover handlers in other modules. """
        autodiscover_modules(self.name)
