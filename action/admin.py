""" Action app admin module. """
from django.contrib import admin


class ActionAdmin(admin.ModelAdmin):
    """ An abstract class for actions. """

    def channel_repr(self, obj):
        """ Action channel link. """
        # pylint: disable=no-self-use
        return obj.get_link()

    channel_repr.short_description = 'Channel'
    list_display = ('callee_name', 'extension', 'channel_repr')
    exclude = ('channel',)
