""" Conference app admin module. """
from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from conference.models import Conference


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    """ Conference model admin tweaks. """

    def conference_link(self, obj):
        """ Conference link. """
        # pylint: disable=no-self-use
        return format_html(
            '<a href="https://%s/c/%s">link</a>' % (
                settings.PBX_HOSTNAME,
                obj.channel_id,
            )
        )

    conference_link.short_description = ''

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
        'channel',
    )
    list_display = (
        'topic',
        'channel',
        'conference_link',
        'clients_link',
    )
