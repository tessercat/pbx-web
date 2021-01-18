""" Peers app views module. """
from datetime import timedelta
import os
from uuid import UUID
from fnmatch import fnmatch
from django.conf import settings
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.detail import BaseDetailView, DetailView
from common.decorators import cache_public
from verto.models import Channel, Client


class IndexView(TemplateView):
    """ Public peer channels index view. """

    template_name = 'peers/index.html'

    def public_channels(self):
        """ Return public channel query set. """
        # pylint: disable=no-self-use
        channels = Channel.objects.filter(realm='peers', is_public=True)
        for channel in channels:
            channel.url = 'https://%s/%s/%s' % (
                settings.PBX_HOSTNAME, channel.realm, channel.channel_id
            )
        return channels


@method_decorator(cache_public(60 * 15), name='dispatch')
class AboutView(TemplateView):
    """ About the peer channels app view. """
    template_name = 'peers/about.html'


class PeerView(DetailView):
    """ Peer client channel view. """
    model = Channel
    slug_field = 'channel_id'
    slug_url_kwarg = 'channel_id'
    static_dir = os.path.join(settings.BASE_DIR, 'static', 'peers', 'js')

    def _static_path(self, target):
        pattern = '%s-?????.js' % target
        for filename in os.listdir(self.static_dir):
            if fnmatch(filename, pattern):
                return 'peers/js/%s' % filename
        return None

    def adapter_path(self):
        """ Return the adapter file's static path. """
        return self._static_path('adapter')

    def client_path(self):
        """ Return the peer client's static path. """
        return self._static_path('peer')

    def get_object(self, queryset=None):
        """ Raise 404 when auth realm is not correct. """
        channel = super().get_object()
        if channel.realm != 'peers':
            raise Http404
        return channel


class SessionView(BaseDetailView):
    """ Peer client session registration view. """
    model = Channel
    slug_field = 'channel_id'
    slug_url_kwarg = 'channel_id'

    def get_context_data(self, **kwargs):
        """ Return clientId and password for the sessionId in request args.

        Raise 404 if a client exists for the session but the session is
        expired, or return None for all other errors.

        Return a dict of clientId and password for an existing, unexpired
        session, or from a new client whose session expires in two weeks.
        """
        session_id = self.request.GET.get('sessionId')
        if not session_id:
            return None
        try:
            UUID(session_id, version=4)
        except ValueError:
            return None
        try:
            client = Client.objects.get(session_id=session_id)
            if client.channel != self.object:
                return None
            if client.created + timedelta(days=14) < timezone.now():
                raise Http404
        except Client.DoesNotExist:
            client = Client.objects.create(
                channel=self.object,
                session_id=session_id
            )
        return {
            'sessionId': str(client.session_id),
            'clientId': str(client.client_id),
            'password': str(client.password)
        }

    def get_object(self, queryset=None):
        """ Raise 404 when auth realm is not correct. """
        channel = super().get_object()
        if channel.realm != 'peers':
            raise Http404
        return channel

    def render_to_response(self, context):
        """ Return context as JSON response or 403. """
        # pylint: disable=no-self-use
        if not context:
            return HttpResponseForbidden()
        return JsonResponse(context)
