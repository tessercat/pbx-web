""" Intercom app models module. """
import logging
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from intercom.apps import intercom_settings
from sofia.models import Intercom, Gateway
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


class GatewayExtension(models.Model):
    """ A combined extension/action to call a dialed number matching the
    extension's expression through the extension's Gateway. """

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

    template = 'intercom/gateway.xml'

    name = models.CharField(max_length=50)
    expression = models.CharField(max_length=50)
    intercom = models.ForeignKey(
        Intercom,
        on_delete=models.CASCADE
    )
    cid_name = models.CharField(
        max_length=50
    )
    cid_number = models.CharField(
        max_length=50
    )
    gateway = models.ForeignKey(
        Gateway,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} ({self.intercom})'


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

    def get_dialstring(self):
        """ Return the dialstring for the bridge template. """
        lines = []

        logger = logging.getLogger('django.server')
        for line in self.line_set.all():
            logger.info(line)

        dialstring = '[%s,%s]sofia/gateway/%s/%s'
        cid_name = 'origination_caller_id_name=%s'
        cid_number = 'origination_caller_id_number=%s'
        for line in self.outsideline_set.all():
            lines.append(
                dialstring % (
                    cid_name % line.cid_name,
                    cid_number % line.cid_number,
                    line.gateway.domain,
                    line.phone_number
                )
            )
        return ':_:'.join(lines)


class Line(models.Model):
    """ A username/password registration for an Intercom profile. Lines are
    able to call any of their Intercom's Extensions, and they are able to call
    external numbers via their GatewayExtensions. Lines receive calls when
    their Bridges are called. """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='per_intercom_unique_username',
                fields=['username', 'intercom']
            ),
        ]

    name = models.CharField(max_length=15)
    username = models.SlugField(
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
    gateway_extensions = models.ManyToManyField(
        GatewayExtension,
        blank=True,
    )
    registered = models.DateTimeField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.name} ({self.intercom})'


class OutsideLine(models.Model):
    """ An external phone number and a Gateway. Calls to Bridges that
    reference an OutsideLine dial the external number through the line's
    Gateway. """

    phone_number = models.CharField(
        unique=True,
        max_length=50,
    )
    cid_name = models.CharField(
        max_length=50
    )
    cid_number = models.CharField(
        max_length=50
    )
    gateway = models.ForeignKey(
        Gateway,
        on_delete=models.CASCADE
    )
    bridges = models.ManyToManyField(
        Bridge,
        blank=True,
    )

    def __str__(self):
        return f'{self.phone_number} ({self.cid_name} {self.cid_number})'


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
