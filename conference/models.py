""" Conference app models module. """
from django.db import models
from action.models import Action


class Conference(Action):
    """ A conference action. """
    template = 'conference/conference.xml'
    data = models.SlugField(
        max_length=50,
    )
