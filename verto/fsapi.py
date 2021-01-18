""" Verto app Fsapi request handler module. """
from uuid import UUID
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from verto.models import Client
from fsapi.registries import FsapiHandler, register_fsapi_handlers


class ProfileHandler(FsapiHandler):
    """ Verto profile config request handler. """

    def __init__(self):
        super(ProfileHandler, self).__init__(
            key_value='verto.conf',
            section='configuration',
        )

    def process(self, request):
        """ Process verto profile configuration requests. """
        template = 'verto/verto.conf.xml'
        context = {
            'debug_level': 10,
            'directory_domain': settings.PBX_HOSTNAME,
            'verto_port': settings.VERTO_PORT,
        }
        return template, context


class AuthHandler(FsapiHandler):
    """ Client auth request handler. """

    def __init__(self):
        super(AuthHandler, self).__init__(
            action='jsonrpc-authenticate',
            domain=settings.PBX_HOSTNAME,
            section='directory',
        )

    def process(self, request):
        """ Process verto client auth requests by auth realm (app name)
        from the auth registry. """
        try:
            UUID(request.POST['user'], version=4)
        except ValueError:
            raise Http404
        client = get_object_or_404(Client, client_id=request.POST['user'])
        auth_handler = settings.VERTO_AUTH_HANDLERS.registry.get(
            client.channel.realm
        )
        if auth_handler:
            self.logger.info(
                'Processing %s.', auth_handler.__class__.__name__,
            )
            return auth_handler.process(request, client)
        raise Http404


class LoginEventHandler(FsapiHandler):
    """ Handle verto client login events. """

    def __init__(self):
        super(LoginEventHandler, self).__init__(
            action='verto_client_login',
        )

    def process(self, request):
        """ Process verto client login events and return "punt" on error.
        If the login is OK, set the Client object's connected timestamp.

        Assume that FreeSWITCH POSTs these events only on login success
        and therefore that it's safe to assume that a client object exists
        for the POSTed client_id and that it must be a UUID since the
        Client model enforces UUID client_id.

        Assume that if the POSTed session_id is not a UUID, that testing
        it against the expected value will catch the error since the
        Client model enforces UUID session_id.
        """
        template = 'verto/verto.event.txt'
        client = Client.objects.get(client_id=request.POST['client_id'])
        if str(client.session_id) != request.POST['session_id']:
            self.admin_logger.error(
                'Session ID mismatch', extra={'request': request}
            )
            self.logger.info(
                'Session ID mismatch for client %s %s expected %s.',
                client, request.POST['session_id'], client.session_id
            )
            return template, {'response': 'punt'}
        # Punt if public channel is full.
        client.connected = timezone.now()
        client.save()
        return template, {'response': 'ok'}


class DisconnectEventHandler(FsapiHandler):
    """ Handle verto client disconnect events. """

    def __init__(self):
        super(DisconnectEventHandler, self).__init__(
            action='verto_client_disconnect',
        )

    def process(self, request):
        """ Process verto client disconnect events and return "ok". If a
        client for the login username (client_id) is found, unset the
        client's connected timestamp. """
        client_id = request.POST['client_id'].split('@')[0]
        try:
            UUID(client_id, version=4)
        except ValueError:
            raise Http404
        client = get_object_or_404(Client, client_id=client_id)
        template = 'verto/verto.event.txt'
        client.connected = None
        client.save()
        return template, {'response': 'ok'}


register_fsapi_handlers(
    AuthHandler(),
    ProfileHandler(),
    LoginEventHandler(),
    DisconnectEventHandler(),
)
