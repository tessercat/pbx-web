""" Intercom app models module. """
from django.db import models
from sofia.models import SofiaProfile


class Intercom(SofiaProfile):
    """ A SofiaProfile with Lines and Extensions. """


class Line(models.Model):
    """ A username/password Intercom registration. """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='per_intercom_unique_username',
                fields=['username', 'intercom']
            ),
        ]

    # Validate name as whetever CNAM allows?
    # Autogenerate username/password?

    name = models.CharField(max_length=15)
    username = models.SlugField(
        max_length=50,
    )
    password = models.CharField(max_length=50)
    intercom = models.ForeignKey(
        'intercom.Intercom',
        on_delete=models.CASCADE
    )
    registered = models.DateTimeField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.intercom} - {self.name}'
