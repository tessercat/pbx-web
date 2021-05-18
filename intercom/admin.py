""" Intercom app admin module. """
from django.conf import settings
from django.contrib import admin
from intercom.models import Intercom, Line


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


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    """ Line model admin tweaks. """
    exclude = ('registered',)
    list_display = (
        'name',
        'intercom',
        'username', 'password',
        'registered'
    )
