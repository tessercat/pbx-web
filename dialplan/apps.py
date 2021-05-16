""" Dialplan app config module. """
from django.apps import AppConfig


dialplan_settings = {}


class DialplanConfig(AppConfig):
    """ Dialplan app config. """
    name = 'dialplan'

    def ready(self):
        """ Autodiscover handlers in other modules. """
        # pylint: disable=import-outside-toplevel
        import logging
        from django.utils.module_loading import autodiscover_modules
        from dialplan.models import Action

        autodiscover_modules('dialplan')

        # Configure action_names.
        action_names = []
        for subclass in Action.__subclasses__():
            action_names.append(subclass._meta.model_name)
        dialplan_settings['action_names'] = action_names
        logger = logging.getLogger('django.server')
        for name in action_names:
            logger.info('%s %s', self.name, name)
