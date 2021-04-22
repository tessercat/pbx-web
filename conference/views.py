""" Conference app views module. """
from datetime import timedelta
from uuid import UUID
from django.conf import settings
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.detail import BaseDetailView, DetailView
from conference.models import Conference
from verto.models import Channel, Client


def is_conference(channel):
    """ Return True if the channel's application is a conference. """
    try:
        app = channel.application
    except Channel.DoesNotExist:
        return False
    if isinstance(app, Conference):
        return True
    return False


class IndexView(TemplateView):
    """ Conference app index view. """
    template_name = 'conference/index.html'

    def get_context_data(self, **kwargs):
        """ Insert data into template context. """
        context = super().get_context_data(**kwargs)
        context['page_title'] = settings.PBX_HOSTNAME
        context['common_css'] = settings.COMMON_CSS
        return context


class ClientView(DetailView):
    """ Conference verto client channel view. """
    model = Channel
    slug_field = 'channel_id'
    slug_url_kwarg = 'channel_id'
    template_name = 'conference/verto-client.html'

    def get_context_data(self, **kwargs):
        """ Insert data into template context. """
        context = super().get_context_data(**kwargs)
        context['page_title'] = context['object'].application.topic
        context['conference_css'] = settings.CONFERENCE_CSS
        context['adapter_js'] = settings.CONFERENCE_ADAPTER_JS
        context['client_js'] = settings.CONFERENCE_CLIENT_JS
        context['stun_port'] = settings.STUN_PORT
        return context

    def get_object(self, queryset=None):
        """ Raise 404 when application is not correct. """
        channel = super().get_object()
        if is_conference(channel):
            return channel
        raise Http404


class SessionView(BaseDetailView):
    """ Conference client session registration view. """
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
        """ Raise 404 when application is not correct. """
        channel = super().get_object()
        if is_conference(channel):
            return channel
        raise Http404

    def render_to_response(self, context):
        """ Return context as JSON response or 403. """
        # pylint: disable=no-self-use
        if not context:
            return HttpResponseForbidden()
        return JsonResponse(context)
