""" Call app models module. """
from django.db import models
from dialplan.models import Action


class GroupCall(Action):
    """ An Action to a group of Lines. """
    template = 'call/group.xml'

    extension = models.OneToOneField(
        'intercom.Extension',
        on_delete=models.CASCADE,
    )
    lines = models.ManyToManyField(
        'intercom.Line',
    )


class InboundTransfer(Action):
    """ An Action transfer from Gateway to Extension. """
    template = 'call/transfer.xml'

    did_number = models.OneToOneField(
        'gateway.DidNumber',
        on_delete=models.CASCADE
    )
    extension = models.OneToOneField(
        'intercom.Extension',
        on_delete=models.CASCADE
    )


class OutboundCall(Action):
    """ An Action out through a Gateway. """
    template = 'call/outbound.xml'

    extension = models.OneToOneField(
        'intercom.Extension',
        on_delete=models.CASCADE,
    )
    number = models.CharField(
        blank=True,
        max_length=50,
    )
    gateway = models.ForeignKey(
        'gateway.Gateway',
        on_delete=models.CASCADE
    )
