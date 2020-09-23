""" Peers app verto auth handler module. """
from channels.handlers import AuthHandler, register_handler


class PeerAuthHandler(AuthHandler):
    """ Verto auth handler for peer sessions. """
    # pylint: disable=too-few-public-methods

    def process(self, request, session):
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
                session.channel.channel_id,
            ),
            'allowed_jsapi_commands': [],
            'user_id': session.client_id,
            'password': session.password,
        }
        return template, context


register_handler('peers', PeerAuthHandler())
