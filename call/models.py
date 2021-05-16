""" Call app models module. """
from django.db import models
from action.models import Action


class LineCall(Action):
    """ An Action that calls a single Line. """
    template = 'call/line.xml'

    extension = models.OneToOneField(
        'intercom.Extension',
        on_delete=models.CASCADE
    )
    line = models.OneToOneField(
        'intercom.Line',
        on_delete=models.CASCADE
    )


class GroupCall(Action):
    """ An Action that sim-rings a group of Lines. """
    template = 'call/group.xml'

    extension = models.OneToOneField(
        'intercom.Extension',
        on_delete=models.CASCADE
    )
    lines = models.ManyToManyField(
        'intercom.Line',
    )


class OutboundCall(Action):
    """ An Action to call out through a Gateway. """
    template = 'call/outbound.xml'

    extension = models.OneToOneField(
        'intercom.Extension',
        on_delete=models.CASCADE
    )
    number = models.CharField(
        blank=True,
        max_length=50,
    )
    gateway = models.ForeignKey(
        'gateway.Gateway',
        on_delete=models.CASCADE
    )


class InboundTransfer(Action):
    """ An Action to transfer a Gateway call to an Extension. """
    template = 'call/transfer.xml'

    did_number = models.OneToOneField(
        'gateway.DidNumber',
        on_delete=models.CASCADE
    )
    extension = models.ForeignKey(
        'intercom.Extension',
        on_delete=models.CASCADE
    )
