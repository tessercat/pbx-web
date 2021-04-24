""" Directory app config module. """
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class DirectoryConfig(AppConfig):
    """ Directory app config. """
    name = 'directory'

    def ready(self):
        """ Autodiscover handlers in other modules. """
        autodiscover_modules('directory')
