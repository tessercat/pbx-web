""" Peers app admin module. """
from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from verto.models import Channel, Client


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    """ Channel model admin tweaks. """

    def channel_link(self, obj):
        """ Channel ID link in list display. """
        # pylint: disable=no-self-use
        return format_html(
            '<a href="https://%s/%s/%s">%s</a>' % (
                settings.PBX_HOSTNAME,
                obj.realm,
                obj.channel_id,
                obj.channel_id,
            )
        )

    channel_link.short_description = 'Channel'

    def clients_link(self, obj):
        """ Clients link in list display. """
        # pylint: disable=no-self-use
        return format_html(
            '<a href="%s?%s">clients</a>' % (
                reverse('admin:verto_client_changelist'),
                'q=%s' % obj.channel_id
            )
        )

    clients_link.short_description = ''

    fields = (
        'topic',
        'realm',
    )
    list_display = (
        'topic',
        'realm',
        'channel_link',
        'clients_link',
    )
    search_fields = (
        'channel_id__exact',
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """ Client model admin tweaks. """

    def short_client_id(self, obj):
        """ Return a shortened client ID. """
        # pylint: disable=no-self-use
        return str(obj.client_id)[0:5]

    short_client_id.short_description = 'Client ID'

    ordering = ('-connected', '-created')
    list_display = (
        'short_client_id',
        'channel',
        'created',
        'connected'
    )
    search_fields = (
        'channel__channel_id__exact',
    )
