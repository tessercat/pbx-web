""" Intercom app models module. """
from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.html import format_html
from dialplan.apps import dialplan_settings
from dialplan.models import Action
from sofia.models import SofiaProfile
from verto.models import Channel


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
        Intercom,
        on_delete=models.CASCADE
    )
    registered = models.DateTimeField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.intercom} - {self.name}'


class Extension(models.Model):
    """ An Intercom, an extension number/expression an optional Channel. """

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

    def get_action(self):
        """ Return the Extension's subclassed Action object. """
        for name in dialplan_settings['action_names']:
            if hasattr(self, name):
                return getattr(self, name)
        return None

    def matches(self, number):
        """ Return True for a PCRE extension and the number matches. """
        return False

    name = models.CharField(max_length=15)
    extension_number = models.CharField(max_length=50)
    intercom = models.ForeignKey(
        Intercom,
        on_delete=models.CASCADE
    )
    pcre_match = models.BooleanField(default=False)
    web_enabled = models.BooleanField(default=False)
    channel = models.OneToOneField(
        Channel,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.intercom} - {self.extension_number} {self.name}'


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
    instance.channel.delete()


class CallGroup(Action):
    """ A call Action to a group of Lines. """
    template = 'intercom/group.xml'
    intercom_action = True

    extension = models.OneToOneField(
        Extension,
        on_delete=models.CASCADE,
    )
    lines = models.ManyToManyField(Line)


class OutboundCall(Action):
    """ A call Action out through a Gateway. """
    template = 'intercom/outbound.xml'
    intercom_action = True

    extension = models.OneToOneField(
        Extension,
        on_delete=models.CASCADE,
    )
    phone_number = models.CharField(
        blank=True,
        max_length=50,
    )
    gateway = models.ForeignKey(
        'gateway.Gateway',
        on_delete=models.CASCADE
    )
