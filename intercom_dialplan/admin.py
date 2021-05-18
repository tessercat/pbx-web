""" Intercom app admin module. """
from django.contrib import admin
from intercom_dialplan.models import (
    Extension,
    GroupCallExtension,
    OutboundCallExtension,
    OutboundCallMatcher,
    InboundTransfer
)


@admin.register(Extension)
class ExtensionAdmin(admin.ModelAdmin):
    """ Extension model admin tweaks. """
    exclude = ('channel',)


@admin.register(GroupCallExtension)
class GroupCallExtensionAdmin(admin.ModelAdmin):
    """ GroupCallExtension model admin tweaks. """
    list_display = ('extension',)


@admin.register(OutboundCallExtension)
class OutboundCallExtensionAdmin(admin.ModelAdmin):
    """ OutboundCallExtension model admin tweaks. """
    list_display = (
        'extension', 'outbound_number',
        'caller_id_number', 'caller_id_name',
        'gateway'
    )


@admin.register(OutboundCallMatcher)
class OutboundCallMatcherAdmin(admin.ModelAdmin):
    """ OutboundCallMatcher model admin tweaks. """
    list_display = (
        'name', 'expression', 'intercom',
        'caller_id_name', 'caller_id_number',
        'gateway'
    )


@admin.register(InboundTransfer)
class InboundTransferAdmin(admin.ModelAdmin):
    """ InboundTransfer model admin tweaks. """
