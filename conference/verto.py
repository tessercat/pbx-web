""" Conference app verto auth handler module. """
from django.conf import settings
from verto.registries import AuthHandler, register_verto_auth_handler


class ConferenceAuthHandler(AuthHandler):
    """ Verto auth handler for conference clients. """
    # pylint: disable=too-few-public-methods

    def process(self, request, client):
        template = 'conference/verto.auth.xml'
        context = {
            'pbx_hostname': settings.PBX_HOSTNAME,
            'user_id': client.client_id,
            'password': client.password,
        }
        return template, context


register_verto_auth_handler(
    settings.CONFERENCE_AUTH_REALM, ConferenceAuthHandler()
)
