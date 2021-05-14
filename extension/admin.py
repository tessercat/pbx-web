""" Extension app admin module. """
from django.contrib import admin
from extension.models import (
    IntercomNumber, IntercomMatch,
    LineCall, GroupCall, OutboundCall, OutboundMatchCall,
    InboundTransfer
)


class ExtensionAdmin(admin.ModelAdmin):
    """ An extension admin superclass. """
    exclude = ('channel',)


@admin.register(IntercomNumber)
class IntercomNumberAdmin(ExtensionAdmin):
    """ IntercomNumber model admin tweaks. """


@admin.register(IntercomMatch)
class IntercomPatternAdmin(ExtensionAdmin):
    """ IntercomPattern model admin tweaks. """


@admin.register(LineCall)
class LineCallAdmin(ExtensionAdmin):
    """ LineCall model admin tweaks. """


@admin.register(GroupCall)
class GroupCallAdmin(ExtensionAdmin):
    """ GroupCall model admin tweaks. """


@admin.register(OutboundCall)
class OutbounCallAdmin(ExtensionAdmin):
    """ GroupCall model admin tweaks. """


@admin.register(OutboundMatchCall)
class OutboundMatchCallAdmin(ExtensionAdmin):
    """ OutboundMatchCall model admin tweaks. """


@admin.register(InboundTransfer)
class InboundTransferAdmin(ExtensionAdmin):
    """ InboundTransfer model admin tweaks. """
