""" Action app views module. """
from datetime import timedelta
from uuid import UUID
from django.conf import settings
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView, BaseDetailView
from action.apps import action_settings
from verto.models import Channel, Client


class IndexView(TemplateView):
    """ Action app index view. """
    template_name = 'action/index.html'

    def get_context_data(self, **kwargs):
        """ Insert data into template context. """
        context = super().get_context_data(**kwargs)
        context['title'] = settings.PBX_HOSTNAME
        context['css'] = action_settings.get('css')
        return context


class ClientView(DetailView):
    """ Action Channel client view. """
    model = Channel
    slug_field = 'channel_id'
    slug_url_kwarg = 'channel_id'
    template_name = "action/client.html"

    def get_context_data(self, **kwargs):
        """ Insert data into template context. """
        context = super().get_context_data(**kwargs)
        if hasattr(self.object, 'action'):
            action = self.object.action.get_action()
        else:
            raise Http404
        context['title'] = action.callee_name
        context['stun_port'] = settings.STUN_PORT
        context['css'] = action_settings.get('css')
        context['adapter'] = action_settings.get('adapter')
        context['client'] = action_settings.get('client')
        return context


class SessionView(BaseDetailView):
    """ Action Channel client session registration view. """
    model = Channel
    slug_field = 'channel_id'
    slug_url_kwarg = 'channel_id'

    def get_context_data(self, **kwargs):
        """ Return clientId and password for the sessionId in request args.

        Raise 404 if a client exists for the session but the session is
        expired, or return None to raise 403 for all other errors.

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

    def render_to_response(self, context):
        """ Return context as JSON response or 403. """
        # pylint: disable=no-self-use
        if not context:
            return HttpResponseForbidden()
        return JsonResponse(context)