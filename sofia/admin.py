""" Sofia app admin module. """
from django.conf import settings
from django.contrib import admin
from sofia.models import (
    IntercomProfile, SipLine, Extension,
    GatewayProfile, DidNumber
)


@admin.register(IntercomProfile)
class IntercomAdmin(admin.ModelAdmin):
    """ IntercomProfile admin tweaks. """

    def intercom_repr(self, obj):
        """ Return capitalized domain. """
        # pylint: disable=no-self-use
        return obj.domain.capitalize()

    def uri_repr(self, obj):
        """ Return profile SIPS URI. """
        # pylint: disable=no-self-use
        return 'sips:%s:%s' % (settings.PBX_HOSTNAME, obj.port)

    intercom_repr.short_description = 'Intercom'
    uri_repr.short_description = 'URI'
    list_display = ('intercom_repr', 'uri_repr')
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


@admin.register(SipLine)
class SipLineAdmin(admin.ModelAdmin):
    """ SipLine model admin tweaks. """

    # Add links to call groups and page groups.

    exclude = ['registered']
    list_display = (
        'caller_name',
        'intercom',
        'username', 'password',
        'gateway',
        'registered'
    )


@admin.register(Extension)
class ExtensionAdmin(admin.ModelAdmin):
    """ Extension model admin tweaks. """
    list_display = ('number', 'intercom')


@admin.register(GatewayProfile)
class GatewayAdmin(admin.ModelAdmin):
    """ GatewayProfile admin tweaks. """
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


@admin.register(DidNumber)
class DidNumberAdmin(admin.ModelAdmin):
    """ DidNumber model admin tweaks. """
