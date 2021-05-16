""" Action app models module. """
from django.db import models
from action.apps import action_settings


class Action(models.Model):
    """ A named but un-addressed dialplan action. """

    def get_action(self):
        """ Return the subclassed object. """
        for name in action_settings['action_names']:
            if hasattr(self, name):
                return getattr(self, name)
        return None

    # Override in subclasses.
    template = None

    name = models.CharField(max_length=15)
