""" Intercom app models module. """
import re
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from intercom.apps import intercom_settings
from sofia.models import Intercom
from verto.models import Channel


class Extension(models.Model):
    """ A numbered dialplan Action and optional verto Channel. """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_is_unique',
                fields=['extension_number', 'intercom']
            ),
        ]

    def get_action(self):
        """ Return the Extension's Action subtype or None. """
        if hasattr(self, 'action'):
            action = getattr(self, 'action')
            for name in intercom_settings['action_names']:
                if hasattr(action, name):
                    return getattr(action, name)
        return None

    extension_number = models.CharField(max_length=50)
    intercom = models.ForeignKey(
        Intercom,
        on_delete=models.CASCADE
    )
    web_enabled = models.BooleanField(default=False)
    channel = models.OneToOneField(
        Channel,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.extension_number} ({self.intercom})'


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


class OutboundCallerId(models.Model):
    """ An outbound calling name/number. """
    name = models.CharField(
        max_length=50
    )
    phone_number = models.CharField(
        max_length=50
    )

    def __str__(self):
        return f'{self.name} {self.phone_number}'


class OutboundExtension(models.Model):
    """ A combined extension/action for Lines to call through Gateways. """

    def matches(self, dialed_number):
        """ Return the matched phone number or False. """
        match = re.fullmatch(self.expression, dialed_number)
        if match:
            groups = match.groups()
            if groups:
                return groups[0]
            return match.string
        return False

    template = 'intercom/outbound.xml'

    name = models.CharField(max_length=50)
    expression = models.CharField(max_length=50)
    default_caller_id = models.ForeignKey(
        OutboundCallerId,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Action(models.Model):
    """ A concrete named Extension dialplan action. Meant to be subclassed.
    The intercom.apps module enumerates subclasses on app ready, and Extension
    objects provide a get_action method so that dialplan handlers can retrieve
    and process the subclassed action object. """
    template = None

    name = models.CharField(max_length=50)
    extension = models.OneToOneField(
        Extension,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.name} {self.extension}'


class Bridge(Action):
    """ An Action to call the Lines and OutsideLines that reference it. """
    template = 'intercom/bridge.xml'


class Line(models.Model):
    """ A unique username/password registration for the host domain. Lines are
    able to call any of their intercom's Extensions. Lines call extensions of
    other intercoms via InboundTransfers, and they call external numbers via
    OutboundExtensions. Lines receive calls when their Bridges are called. """

    name = models.CharField(max_length=15)
    username = models.SlugField(
        unique=True,
        max_length=50,
    )
    password = models.CharField(max_length=50)
    intercom = models.ForeignKey(
        Intercom,
        on_delete=models.CASCADE
    )
    bridges = models.ManyToManyField(
        Bridge,
        blank=True,
    )
    outbound_extensions = models.ManyToManyField(
        OutboundExtension,
        blank=True,
    )
    outbound_caller_id = models.ForeignKey(
        OutboundCallerId,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    registered = models.DateTimeField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.name} ({self.intercom})'


class OutsideLine(models.Model):
    """ An external phone number. Calls to Bridges that reference an
    OutsideLine call the phone number through a Gateway. """
    note = models.CharField(
        max_length=50,
    )
    phone_number = models.CharField(
        unique=True,
        max_length=50,
    )
    default_caller_id = models.ForeignKey(
        OutboundCallerId,
        on_delete=models.CASCADE
    )
    bridges = models.ManyToManyField(
        Bridge,
        blank=True,
    )

    def __str__(self):
        return f'{self.note} {self.phone_number}'


class InboundTransfer(models.Model):
    """ A dialplan action to transfer external calls to an Extension. """
    template = 'intercom/transfer.xml'

    phone_number = models.CharField(
        unique=True,
        max_length=50,
    )
    transfer_extension = models.ForeignKey(
        Extension,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.phone_number} {self.transfer_extension}'
