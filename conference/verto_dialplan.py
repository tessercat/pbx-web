""" Conference app verto dialplan request handler module. """
from verto.registries import (
    VertoDialplanHandler,
    register_verto_dialplan_handler,
)
from conference.models import Conference


class ConferenceHandler(VertoDialplanHandler):
    """ Verto dialplan handler for conference clients. """
    # pylint: disable=too-few-public-methods

    def process(self, request, client):
        template = 'conference/verto-dialplan.xml'
        context = {
            'dest': client.channel.channel_id,
            'confname': client.channel.channel_id,
        }
        return template, context


register_verto_dialplan_handler(
    Conference.__name__,
    ConferenceHandler()
)
