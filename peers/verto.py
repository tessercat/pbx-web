""" Peers verto auth handler module. """
from verto.registries import AuthHandler, register_verto_auth_handler


class PeerAuthHandler(AuthHandler):
    """ Verto auth handler for peer clients. """
    # pylint: disable=too-few-public-methods

    def process(self, request, client):
        template = 'peers/verto.auth.xml'
        context = {
            'directory_domain': request.POST['domain'],
            'allowed_methods': (
                'echo',
                'verto.subscribe',
                'verto.broadcast',
                'verto.info',
            ),
            'allowed_event_channels': (
                client.channel.channel_id,
            ),
            'allowed_jsapi_commands': [],
            'user_id': client.client_id,
            'password': client.password,
        }
        return template, context


register_verto_auth_handler('peers', PeerAuthHandler())
