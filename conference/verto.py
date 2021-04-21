""" Conference app verto request handler module. """
from django.conf import settings
from verto.registries import (
    VertoDialplanHandler,
    VertoDirectoryHandler,
    register_verto_dialplan_handler,
    register_verto_directory_handler
)


class ConferenceVertoDirectoryHandler(VertoDirectoryHandler):
    """ Verto directory handler for conference clients. """
    # pylint: disable=too-few-public-methods

    def process(self, request, client):
        template = 'conference/directory.xml'
        context = {
            'pbx_hostname': settings.PBX_HOSTNAME,
            'user_id': client.client_id,
            'password': client.password,
        }
        return template, context


register_verto_directory_handler(
    settings.CONFERENCE_AUTH_REALM,
    ConferenceVertoDirectoryHandler()
)


class ConferenceVertoDialplanHandler(VertoDialplanHandler):
    """ Verto dialplan handler for conference clients. """
    # pylint: disable=too-few-public-methods

    def process(self, request, client):
        template = 'conference/dialplan.xml'
        context = {
            'pbx_hostname': settings.PBX_HOSTNAME,
            'user_id': client.client_id,
            'password': client.password,
        }
        return template, context


register_verto_dialplan_handler(
    settings.CONFERENCE_AUTH_REALM,
    ConferenceVertoDialplanHandler()
)
