""" Intercom app config module. """
from django.apps import AppConfig


intercom_dialplan_settings = {}


class IntercomDialplanConfig(AppConfig):
    """ Intercom dialplan app config. """
    name = 'intercom_dialplan'
    verbose_name = 'Dialplan'

    def ready(self):
        """ Config on app ready. """
        # pylint: disable=import-outside-toplevel
        import logging
        from intercom_dialplan.models import IntercomAction

        # Configure action_names.
        logger = logging.getLogger('django.server')
        action_names = []
        for subclass in IntercomAction.__subclasses__():
            action_names.append(subclass._meta.model_name)
        intercom_dialplan_settings['action_names'] = action_names
        for name in action_names:
            logger.info('%s %s', self.name, name)
