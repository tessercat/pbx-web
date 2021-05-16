""" Dialplan app models module. """
from django.db import models
from dialplan.apps import dialplan_settings


class Action(models.Model):
    """ A dialplan action superclass/table. """

    def get_action(self):
        """ Return the subclassed object. """
        for name in dialplan_settings['action_names']:
            if hasattr(self, name):
                return getattr(self, name)
        return None

    # Override in subclasses.
    template = None

    name = models.CharField(max_length=15)
