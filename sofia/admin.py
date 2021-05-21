""" Intercom app admin module. """
from django.conf import settings
from django.contrib import admin
from sofia.models import Intercom, Gateway, AclAddress


@admin.register(Intercom)
class IntercomAdmin(admin.ModelAdmin):
    """ Intercom model admin tweaks. """

    def uri_repr(self, obj):
        """ Return profile SIPS URI. """
        # pylint: disable=no-self-use
        return f'sips:{settings.PBX_HOSTNAME}:{obj.port}'

    uri_repr.short_description = 'URI'
    list_display = ('domain', 'uri_repr')
    ordering = ('pk',)

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    """ Gateway model admin tweaks. """
    exclude = ('password',)
    list_display = ('domain', 'port')

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False


@admin.register(AclAddress)
class AclAddressAdmin(admin.ModelAdmin):
    """ AclAddress model admin tweaks. """
    list_display = ('address', 'gateway')

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False
