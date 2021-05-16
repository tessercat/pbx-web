""" Extension app admin module. """
from django.contrib import admin
from call.forms import GroupCallForm, OutboundCallForm
from call.models import GroupCall, InboundTransfer, OutboundCall


@admin.register(GroupCall)
class GroupCallAdmin(admin.ModelAdmin):
    """ GroupCall model admin tweaks. """
    form = GroupCallForm
    list_display = ('extension',)


@admin.register(InboundTransfer)
class InboundTransferAdmin(admin.ModelAdmin):
    """ InboundTransfer model admin tweaks. """
    list_display = ('did_number', 'extension')


@admin.register(OutboundCall)
class OutboundCallAdmin(admin.ModelAdmin):
    """ GroupCall model admin tweaks. """
    form = OutboundCallForm
    list_display = ('extension', 'gateway', 'number')
