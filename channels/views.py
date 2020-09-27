""" Channels app views module. """
from django.conf import settings
from django.views.generic.base import TemplateView
from channels.models import Channel


class IndexView(TemplateView):
    """ Channels index view. """

    template_name = 'channels/index.html'

    def public_channels(self):
        """ Return the query set of public channels. """
        # pylint: disable=no-self-use
        channels = Channel.objects.filter(is_public=True)
        for channel in channels:
            channel.url = 'https://%s/%s/%s' % (
                settings.PBX_HOSTNAME, channel.realm, channel.channel_id
            )
        return channels
