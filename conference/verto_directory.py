""" Conference app verto directory request handler module. """
from django.conf import settings
from verto.registries import (
    VertoDirectoryHandler,
    register_verto_directory_handler
)
from conference.models import Conference


class ConferenceHandler(VertoDirectoryHandler):
    """ Verto directory handler for conference clients. """
    # pylint: disable=too-few-public-methods

    def process(self, request, client):
        template = 'conference/verto-directory.xml'
        context = {
            'user_id': client.client_id,
            'password': client.password,
        }
        return template, context


register_verto_directory_handler(
    Conference.__name__,
    ConferenceHandler()
)
