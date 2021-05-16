""" Action app config module. """
from django.apps import AppConfig


action_settings = {}


class ActionConfig(AppConfig):
    """ Action app config. """
    name = 'action'

    def ready(self):
        """ Init app on ready. """
        # pylint: disable=import-outside-toplevel
        import logging
        from action.models import Action

        # Configure action_names.
        action_names = []
        for subclass in Action.__subclasses__():
            action_names.append(subclass._meta.model_name)
        action_settings['action_names'] = action_names
        logger = logging.getLogger('django.server')
        for name in action_names:
            logger.info('%s %s', self.name, name)
