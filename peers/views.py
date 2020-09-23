""" Peers app views module. """
from datetime import timedelta
import os
from uuid import UUID
from fnmatch import fnmatch
from django.conf import settings
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.views.generic.detail import BaseDetailView, DetailView
from channels.models import Channel, Client


class SessionsView(BaseDetailView):
    """ Peer channel session registration view. """
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


class ChannelView(DetailView):
    """ Peers channel object detail view. """
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
