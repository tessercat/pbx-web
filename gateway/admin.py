""" Gateway app admin module. """
from django.contrib import admin
from gateway.models import Gateway, AclAddress, DidNumber, InboundTransfer


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


@admin.register(DidNumber)
class DidNumberAdmin(admin.ModelAdmin):
    """ DidNumber model admin tweaks. """
    list_display = ('phone_number', 'gateway')


@admin.register(InboundTransfer)
class InboundTransferAdmin(admin.ModelAdmin):
    """ InboundTransfer model admin tweaks. """
    list_display = ('did_number', 'extension')
