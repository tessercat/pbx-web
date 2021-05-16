""" Dialplan app models module. """
from django.db import models


class Action(models.Model):
    """ A dialplan action template. """
    template = None
