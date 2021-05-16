""" Extension app admin module. """
from django.contrib import admin
from call.models import LineCall, GroupCall, OutboundCall, InboundTransfer


@admin.register(LineCall)
class LineCallAdmin(admin.ModelAdmin):
    """ LineCall model admin tweaks. """


@admin.register(GroupCall)
class GroupCallAdmin(admin.ModelAdmin):
    """ GroupCall model admin tweaks. """


@admin.register(OutboundCall)
class OutboundCallAdmin(admin.ModelAdmin):
    """ GroupCall model admin tweaks. """


@admin.register(InboundTransfer)
class InboundTransferAdmin(admin.ModelAdmin):
    """ InboundTransfer model admin tweaks. """
