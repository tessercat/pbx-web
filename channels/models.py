""" Channels app models module. """
import uuid
from django.db import models
from django.urls import reverse


class Channel(models.Model):
    """ A URL UUID, a topic, an auth realm and public/private status. """

    def get_absolute_url(self):
        """ Return channel link.. """
        return reverse('channel', kwargs={'channel': self.pk})

    channel_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    topic = models.CharField(
        max_length=100,
    )
    is_public = models.BooleanField(
        default=False,
    )
    realm = models.SlugField()
    # client_set.all();

    def __str__(self):
        return str(self.topic)


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
        return str(self.client_id)[0:5]
