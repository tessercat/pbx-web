""" Extension app admin module. """
from django.contrib import admin
from extension.admin import ActionAdmin
from call.models import (
    LineCall, GroupCall, OutboundCall, OutboundMatchCall,
    InboundTransfer
)


@admin.register(LineCall)
class LineCallAdmin(ActionAdmin):
    """ LineCall model admin tweaks. """


@admin.register(GroupCall)
class GroupCallAdmin(ActionAdmin):
    """ GroupCall model admin tweaks. """


@admin.register(OutboundCall)
class OutbounCallAdmin(ActionAdmin):
    """ GroupCall model admin tweaks. """


@admin.register(OutboundMatchCall)
class OutboundMatchCallAdmin(ActionAdmin):
    """ OutboundMatchCall model admin tweaks. """


@admin.register(InboundTransfer)
class InboundTransferAdmin(ActionAdmin):
    """ InboundTransfer model admin tweaks. """
