""" Verto app admin module. """
from django.contrib import admin
from verto.models import Channel, Client


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    """ Channel model admin tweaks. """
    list_display = ('channel_id',)

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """ Client model admin tweaks. """
    list_display = ('client_id', 'channel', 'created', 'connected')

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False
