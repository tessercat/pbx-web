""" Verto app models module. """
import uuid
from django.db import models


class Channel(models.Model):
    """ A channel ID. """

    channel_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    # client_set.all();

    def __str__(self):
        """ A shortened channel ID. """
        return str(self.channel_id)[0:8]


class Client(models.Model):
    """ Client and session IDs, a password and timestamps for a channel. """

    client_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    password = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    channel = models.ForeignKey(
        'Channel',
        on_delete=models.CASCADE,
    )
    session_id = models.UUIDField(
        editable=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    connected = models.DateTimeField(
        blank=True,
        null=True,
    )

    def __str__(self):
        """ A shortened client ID. """
        return str(self.client_id)[0:8]
