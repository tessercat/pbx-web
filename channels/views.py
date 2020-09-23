""" Channels app views module. """
import os
from markdown import markdown
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from common.decorators import cache_public
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


@method_decorator(cache_public(60 * 15), name='dispatch')
class AboutView(TemplateView):
    """ About channels view. """
    template_name = 'channels/about.html'

    def about(self):
        """ Return about page HTML content. """
        # pylint: disable=no-self-use
        path = os.path.join(
            settings.BASE_DIR, 'channels', 'markdown', 'about.md',
        )
        with open(path) as about_fd:
            return markdown(about_fd.read())
