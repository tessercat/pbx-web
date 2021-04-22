""" Verto app admin module. """
from django.contrib import admin
from verto.models import Channel, Client


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    """ Channel model admin tweaks. """

    def channel_name(self, obj):
        """ Channel link in list display. """
        # pylint: disable=no-self-use
        return str(obj)

    channel_name.short_description = 'Channel'

    def application_link(self, obj):
        """ Channel application link. """
        # pylint: disable=no-self-use
        try:
            return obj.application.__class__.__name__
        except Channel.DoesNotExist:
            return ''

    application_link.short_description = 'Application'

    list_display = (
        'channel_name',
        'application_link',
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """ Client model admin tweaks. """

    ordering = ('-connected', '-created')
    list_display = (
        'channel',
        'created',
        'connected'
    )
    search_fields = (
        'channel__channel_id__exact',
    )
