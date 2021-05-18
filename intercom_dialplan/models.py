""" Intercom dialplan app models module. """
from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.html import format_html
from verto.models import Channel


class Extension(models.Model):
    """ An Intercom, an extension number and an optional Channel. """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_is_unique',
                fields=['extension_number', 'intercom']
            ),
        ]

    def channel_link(self):
        """ Return a link to the channel. """
        return format_html(
            '<a href="https://%s/%s" title="Open the channel">%s</a>' % (
                settings.PBX_HOSTNAME,
                self.channel.channel_id,
                self.channel
            )
        )

    name = models.CharField(max_length=15)
    extension_number = models.CharField(max_length=50)
    intercom = models.ForeignKey(
        'intercom.Intercom',
        on_delete=models.CASCADE
    )
    # Validate PCRE can't be web-enabled?
    web_enabled = models.BooleanField(default=False)
    channel = models.OneToOneField(
        Channel,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.extension_number} {self.name} ({self.intercom})'


@receiver(signals.post_save, sender=Extension)
def post_save_handler(sender, instance, created, **kwargs):
    """ Add/delete channel on instance save. """
    # pylint: disable=unused-argument
    if instance.channel and not instance.web_enabled:
        instance.channel.delete()
    elif instance.web_enabled and not instance.channel:
        instance.channel = Channel.objects.create()
        instance.save()


@receiver(signals.post_delete, sender=Extension)
def post_delete_handler(sender, instance, **kwargs):
    """ Delete channel on instance delete. """
    # pylint: disable=unused-argument
    if instance.channel:
        instance.channel.delete()


class IntercomAction(models.Model):
    """ An intercom Extension dialplan action. """
    template = None

    extension = models.OneToOneField(
        Extension,
        on_delete=models.CASCADE,
    )


class GroupCallExtension(IntercomAction):
    """ An extension to call a group of Lines. """
    template = 'intercom/group.xml'

    lines = models.ManyToManyField(
        'intercom.Line'
    )


class OutboundCallExtension(IntercomAction):
    """ An extension to call a number through a Gateway. """
    template = 'intercom/outbound.xml'

    caller_id_name = models.CharField(
        max_length=15
    )
    caller_id_number = models.CharField(
        max_length=50
    )
    outbound_number = models.CharField(
        blank=True,
        max_length=50,
    )
    gateway = models.ForeignKey(
        'gateway.Gateway',
        on_delete=models.CASCADE
    )


class OutboundCallMatcher(models.Model):
    """ An extension to call a range of numbers through a Gateway. """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_is_unique',
                fields=['expression', 'intercom']
            ),
        ]

    def matches(self, number):
        """ Return True if the number matches the expression. """
        return number or False

    template = 'intercom/outbound-matcher.xml'

    name = models.CharField(max_length=15)
    expression = models.CharField(max_length=50)
    intercom = models.ForeignKey(
        'intercom.Intercom',
        on_delete=models.CASCADE
    )
    caller_id_name = models.CharField(
        blank=True,  # If blank, send Line name?
        max_length=15
    )
    caller_id_number = models.CharField(
        # Not blank, but can be overridden by Line?
        max_length=50
    )
    gateway = models.ForeignKey(
        'gateway.Gateway',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} ({self.intercom})'


class InboundTransfer(models.Model):
    """ A transfer to an intercom Extension. """
    template = 'gateway/transfer.xml'

    did_number = models.OneToOneField(
        'gateway.DidNumber',
        on_delete=models.CASCADE
    )
    extension = models.ForeignKey(
        Extension,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.did_number} ({self.extension})'
