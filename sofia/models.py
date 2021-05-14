""" Sofia app models module. """
from django.db import models


class SofiaProfile(models.Model):
    """ A generic sofia profile. """
    port = models.IntegerField(
        unique=True
    )
    domain = models.SlugField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.domain
