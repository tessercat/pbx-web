""" Intercom app admin module. """
from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from intercom.models import (
    Extension, GatewayExtension,
    Bridge, Line, OutsideLine, InboundTransfer
)


@admin.register(Extension)
class ExtensionAdmin(admin.ModelAdmin):
    """ Extension model admin tweaks. """

    def action_repr(self, obj):
        """ Return a representation of the action. """
        # pylint: disable=no-self-use
        return obj.get_action().__class__.__name__

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
        'extension_number', 'intercom', 'channel_link',
        'action_repr'
    )


@admin.register(GatewayExtension)
class GatewayExtensionAdmin(admin.ModelAdmin):
    """ GatewayExtension model admin tweaks. """


@admin.register(Bridge)
class BridgeAdmin(admin.ModelAdmin):
    """ Bridge model admin tweaks. """

    def lines_link(self, obj):
        """ Return a link to the Bridge's Lines. """
        # pylint: disable=no-self-use
        url = '/admin/intercom/line/?q=%d' % obj.pk
        return format_html('<a href="%s">lines</a>' % url)

    def outside_lines_link(self, obj):
        """ Return a link to the Bridge's OutsideLines. """
        # pylint: disable=no-self-use
        url = '/admin/intercom/outsideline/?q=%d' % obj.pk
        return format_html('<a href="%s">outside lines</a>' % url)

    lines_link.short_description = ''
    outside_lines_link.short_description = ''

    # Add Line and OutsideLine links?
    list_display = ('name', 'extension', 'lines_link', 'outside_lines_link')


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    """ Line model admin tweaks. """
    # Add link to Bridge search?
    list_display = ('name', 'username', 'password', 'intercom')
    search_fields = ['bridges__pk__exact']


@admin.register(OutsideLine)
class OutsideLineAdmin(admin.ModelAdmin):
    """ OutsideLine model admin tweaks. """
    # Add link to Bridge search?
    list_display = ('phone_number', 'cid_name', 'cid_number', 'gateway')
    search_fields = ['bridges__pk__exact']


@admin.register(InboundTransfer)
class InboundTransferAdmin(admin.ModelAdmin):
    """ InboundTransfer model admin tweaks. """
    list_display = ('phone_number', 'transfer_extension')
