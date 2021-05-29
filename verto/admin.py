""" Verto app admin module. """
from django.contrib import admin
from django.utils.html import format_html
from verto.models import Channel, Client


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    """ Channel model admin tweaks. """

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False

    def channel_repr(self, obj):
        """ Return a shortened Channel ID. """
        # pylint: disable=no-self-use
        return str(obj.channel_id)[:8]

    def clients_link(self, obj):
        """ Return a link to the Channel's Clients. """
        # pylint: disable=no-self-use
        count = obj.client_set.count()
        if count:
            url = '/admin/verto/client/?q=%s' % obj
            return format_html('<a href="%s">%d</a>' % (url, count))
        return None

    channel_repr.short_description = 'Channel'
    clients_link.short_description = 'Clients'
    list_display = ('channel_repr', 'clients_link')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """ Client model admin tweaks. """

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False

    def client_repr(self, obj):
        """ Return a shortened Client ID. """
        # pylint: disable=no-self-use
        return str(obj.client_id)[:8]

    client_repr.short_description = 'Client'
    list_display = ('client_repr', 'channel', 'created', 'connected')
    search_fields = ['channel__channel_id__startswith']
