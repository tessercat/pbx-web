""" Local stream app models module. """
from django.db import models
from action.models import Action


class Playback(Action):
    """ A playback action. """
    template = 'local_stream/playback.xml'

    slug = models.SlugField(
        max_length=50,
        unique=True,
    )


class Recording(Action):
    """ A recording action. """
    template = 'local_stream/recording.xml'

    slug = models.SlugField(
        max_length=50,
        unique=True,
    )
