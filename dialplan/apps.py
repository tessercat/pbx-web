""" Dialplan app config module. """
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from dialplan.registries import dialplan_handler_registry


class DialplanConfig(AppConfig):
    """ Dialplan app config. """
    name = 'dialplan'

    def ready(self):
        """ Autodiscover handlers in other modules. """
        autodiscover_modules(
            'dialplan', register_to=dialplan_handler_registry
        )
