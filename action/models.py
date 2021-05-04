""" Action app models module. """
from django.conf import settings
from django.db import models
from django.utils.html import format_html
from action.apps import action_settings
from sofia.models import Extension
from verto.models import Channel


def post_save_handler(sender, instance, created, **kwargs):
    """ Add channel to instance on creation. """
    # pylint: disable=unused-argument
    if created:
        instance.channel = Channel.objects.create()
        instance.save()


def post_delete_handler(sender, instance, **kwargs):
    """ Delete instance channel on deletion. """
    # pylint: disable=unused-argument
    instance.channel.delete()


class Codec(models.TextChoices):
    """ Codec choices. """
    AUDIO_LOW = 'PCMU', 'LQ audio - Internet and phones'
    AUDIO_HI = 'OPUS', 'HQ audio - Internet only'
    VIDEO = 'OPUS,VP8,H264', 'HQ audio and video - Internet only'


class Action(models.Model):
    """ A sub-classable name, extension and/or channel. """

    # Override in subclasses.
    template = None
    verto_methods = ['echo', 'verto.invite', 'verto.attach']

    # Validate callee_name as whetever CNAM allows.
    callee_name = models.CharField(max_length=15)
    extension = models.OneToOneField(
        Extension,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    channel = models.OneToOneField(
        Channel,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def get_template(self):
        """ Return template. """
        return self.template

    def get_action(self):
        """ Return the subclassed object. """
        for name in action_settings['action_names']:
            if hasattr(self, name):
                return getattr(self, name)
        return None

    def get_link(self):
        """ Return a link to the channel. """
        return format_html(
            '<a href="https://%s/%s" title="Open the channel">%s</a>' % (
                settings.PBX_HOSTNAME,
                self.channel.channel_id,
                self.channel
            )
        )

    def __str__(self):
        return self.get_action().__class__.__name__
