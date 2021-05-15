""" Extension app models module. """
from django.db import models
from extension.models import Action


class LineCall(Action):
    """ An action that calls a single intercom Line. """
    template = 'extension/line.xml'

    extension = models.OneToOneField(
        'extension.Extension',
        on_delete=models.CASCADE
    )
    line = models.OneToOneField(
        'intercom.Line',
        on_delete=models.CASCADE
    )


class GroupCall(Action):
    """ An extension that sim-rings a group of Lines. """
    template = 'extension/group.xml'

    extension = models.OneToOneField(
        'extension.Extension',
        on_delete=models.CASCADE
    )
    lines = models.ManyToManyField(
        'intercom.Line',
    )


class OutboundCall(Action):
    """ A numbered extension that calls through a Gateway. """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_is_unique',
                fields=['extension', 'gateway']
            ),
        ]

    template = 'extension/outbound.xml'

    extension = models.OneToOneField(
        'extension.Extension',
        on_delete=models.CASCADE
    )
    gateway = models.ForeignKey(
        'gateway.Gateway',
        on_delete=models.CASCADE
    )


class OutboundMatchCall(Action):
    """ A pattern-matching Intercom Action with a Gateway. """

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

    template = 'extension/outbound.xml'

    pattern = models.OneToOneField(
        'extension.MatchExtension',
        on_delete=models.CASCADE
    )
    gateway = models.ForeignKey(
        'gateway.Gateway',
        on_delete=models.CASCADE
    )


class InboundTransfer(Action):
    """ An Action to transfer a Gateway call to an Intercom context. """
    template = 'gateway/transfer.xml'

    did_number = models.OneToOneField(
        'gateway.DidNumber',
        on_delete=models.CASCADE
    )
    extension = models.ForeignKey(
        'extension.Extension',
        on_delete=models.CASCADE
    )
