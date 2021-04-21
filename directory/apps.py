""" Directory app config module. """
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from directory.registries import directory_handler_registry


class DirectoryConfig(AppConfig):
    """ Directory app config. """
    name = 'directory'

    def ready(self):
        """ Autodiscover handlers in other modules. """
        autodiscover_modules(
            'directory', register_to=directory_handler_registry
        )
