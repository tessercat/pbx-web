""" Dialplan app config module. """
from django.apps import AppConfig


class DialplanConfig(AppConfig):
    """ Dialplan app config. """
    name = 'dialplan'

    def ready(self):
        """ Autodiscover handlers in other modules. """
        # pylint: disable=import-outside-toplevel
        from django.utils.module_loading import autodiscover_modules

        autodiscover_modules('dialplan')
