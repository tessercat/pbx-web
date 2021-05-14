""" Extension app models module. """
from django.db import models
from django.conf import settings
from django.utils.html import format_html
from extension.apps import extension_settings
from verto.models import Channel


class Codec(models.TextChoices):
    """ Codec choices. """
    AUDIO_LOW = 'PCMU', 'LQ audio - Internet and phones'
    AUDIO_HI = 'OPUS', 'HQ audio - Internet only'
    VIDEO = 'OPUS,VP8,H264', 'HQ audio and video - Internet only'


class Extension(models.Model):
    """ An named but un-addressed dialplan extension. """

    def channel_link(self):
        """ Return a link to the channel. """
        return format_html(
            '<a href="https://%s/%s" title="Open the channel">%s</a>' % (
                settings.PBX_HOSTNAME,
                self.channel.channel_id,
                self.channel
            )
        )

    def get_extension(self):
        """ Return the subclassed object. """
        for name in extension_settings['extension_names']:
            if hasattr(self, name):
                return getattr(self, name)
        return None

    # Override in subclasses.
    template = None

    # Validate name as whetever CNAM allows?
    name = models.CharField(max_length=15)
    publish = models.BooleanField(default=True)
    channel = models.OneToOneField(
        Channel,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )


def post_save_handler(sender, instance, created, **kwargs):
    """ Add/delete channel on instance save. """
    # pylint: disable=unused-argument
    if instance.channel and not instance.publish:
        instance.channel.delete()
    elif instance.publish and not instance.channel:
        instance.channel = Channel.objects.create()
        instance.save()


def post_delete_handler(sender, instance, **kwargs):
    """ Delete channel on instance delete. """
    # pylint: disable=unused-argument
    instance.channel.delete()


# Extensions that match a specfic Intercom number.

class IntercomNumber(models.Model):
    """ An Intercom and a unique number. """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_is_unique',
                fields=['number', 'intercom']
            ),
        ]

    name = models.CharField(max_length=15)
    number = models.CharField(max_length=50)
    intercom = models.ForeignKey(
        'intercom.Intercom',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.intercom} - {self.number} {self.name}'


class LineCall(Extension):
    """ An extension that calls a single intercom Line. """
    template = 'intercom/line.xml'
    number = models.OneToOneField(
        'extension.IntercomNumber',
        on_delete=models.CASCADE
    )
    line = models.OneToOneField(
        'intercom.Line',
        on_delete=models.CASCADE
    )


class GroupCall(Extension):
    """ An extension that sim-rings a group of Lines. """
    template = 'intercom/group.xml'
    number = models.OneToOneField(
        'extension.IntercomNumber',
        on_delete=models.CASCADE
    )
    lines = models.ManyToManyField(
        'intercom.Line',
    )


class OutboundCall(Extension):
    """ A numbered Intercom Extension with a Gateway. """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_is_unique',
                fields=['number', 'gateway']
            ),
        ]

    template = 'intercom/outbound.xml'
    number = models.OneToOneField(
        'extension.IntercomNumber',
        on_delete=models.CASCADE
    )
    gateway = models.ForeignKey(
        'gateway.Gateway',
        on_delete=models.CASCADE
    )


# Extensions that match a regular expression pattern.

class IntercomMatch(models.Model):
    """ An Intercom and a unique pattern. """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_is_unique',
                fields=['pattern', 'intercom']
            ),
        ]

    def matches(self, number):
        """ Return True if the number matches this pattern. """
        return False

    name = models.CharField(max_length=15)
    pattern = models.CharField(max_length=50)
    intercom = models.ForeignKey(
        'intercom.Intercom',
        on_delete=models.CASCADE
    )


class OutboundMatchCall(Extension):
    """ A pattern-matching Intercom Extension with a Gateway. """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_is_unique',
                fields=['pattern', 'gateway']
            ),
        ]

    def matches(self, number):
        """ Return True if the number matches this pattern. """
        return False

    template = 'intercom/outbound.xml'
    pattern = models.OneToOneField(
        'extension.IntercomMatch',
        on_delete=models.CASCADE
    )
    gateway = models.ForeignKey(
        'gateway.Gateway',
        on_delete=models.CASCADE
    )


class InboundTransfer(Extension):
    """ An Extension to transfer a Gateway call to an Intercom context. """
    template = 'gateway/transfer.xml'
    number = models.OneToOneField(
        'gateway.DidNumber',
        on_delete=models.CASCADE
    )
    transfer = models.ForeignKey(
        'extension.IntercomNumber',
        on_delete=models.CASCADE
    )
