""" Intercom app admin module. """
from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from intercom.models import (
    Extension, OutboundExtension,
    Bridge, Line,
    OutboundCallerId,
    OutsideLine, InboundTransfer
)


@admin.register(Extension)
class ExtensionAdmin(admin.ModelAdmin):
    """ Extension model admin tweaks. """

    def action_repr(self, obj):
        """ Return a representation of the action. """
        # pylint: disable=no-self-use
        action = obj.get_action()
        if action:
            return obj.get_action().__class__.__name__
        return None

    def channel_link(self, obj):
        """ Return a link to the channel. """
        # pylint: disable=no-self-use
        if obj.channel:
            return format_html(
                '<a href="https://%s/%s">%s</a>' % (
                    settings.PBX_HOSTNAME,
                    obj.channel.channel_id,
                    obj.channel
                )
            )
        return None

    action_repr.short_description = 'Action'
    channel_link.short_description = 'Channel'

    exclude = ('channel',)
    list_display = (
        'extension_number',
        'intercom',
        'channel_link',
        'action_repr'
    )


@admin.register(OutboundExtension)
class OutboundExtensionAdmin(admin.ModelAdmin):
    """ OutboundExtension model admin tweaks. """
    list_display = ('name', 'expression', 'default_caller_id')


@admin.register(Bridge)
class BridgeAdmin(admin.ModelAdmin):
    """ Bridge model admin tweaks. """

    def lines_link(self, obj):
        """ Return a link to the Bridge's Lines. """
        # pylint: disable=no-self-use
        count = obj.line_set.count()
        if count:
            url = '/admin/intercom/line/?q=%d' % obj.pk
            return format_html('<a href="%s">%d</a>' % (url, count))
        return None

    def outside_lines_link(self, obj):
        """ Return a link to the Bridge's OutsideLines. """
        # pylint: disable=no-self-use
        count = obj.outsideline_set.count()
        if count:
            url = '/admin/intercom/outsideline/?q=%d' % obj.pk
            return format_html('<a href="%s">%d</a>' % (url, count))
        return None

    lines_link.short_description = 'Intercom lines'
    outside_lines_link.short_description = 'Outside lines'

    # Add Line and OutsideLine links?
    list_display = ('name', 'extension', 'lines_link', 'outside_lines_link')


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    """ Line model admin tweaks. """
    # Add link to Bridge search?
    exclude = ('registered',)
    list_display = ('name', 'username', 'password', 'intercom', 'registered')
    search_fields = ['bridges__pk__exact']


@admin.register(OutboundCallerId)
class OutboundCallerIdAdmin(admin.ModelAdmin):
    """ OutboundCallerId model admin tweaks. """
    list_display = ('name', 'phone_number')


@admin.register(OutsideLine)
class OutsideLineAdmin(admin.ModelAdmin):
    """ OutsideLine model admin tweaks. """
    # Add link to Bridge search?
    list_display = ('note', 'phone_number', 'default_caller_id')
    search_fields = ['bridges__pk__exact']


@admin.register(InboundTransfer)
class InboundTransferAdmin(admin.ModelAdmin):
    """ InboundTransfer model admin tweaks. """
    list_display = ('phone_number', 'transfer_extension')
