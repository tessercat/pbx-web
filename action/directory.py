""" Action app directory request handler module. """
from uuid import UUID
from django.http import Http404
from django.shortcuts import get_object_or_404
from directory.registries import DirectoryHandler, register_directory_handler
from verto.models import Client


class ChannelActionAuthHandler(DirectoryHandler):
    """ Handle a verto channel auth request. """

    def get_directory(self, request, domain):
        """ Return template/context for channel auth. """
        client_id = request.POST.get('user')
        if not client_id:
            raise Http404
        try:
            UUID(client_id, version=4)
        except (ValueError) as err:
            raise Http404 from err
        client = get_object_or_404(Client, client_id=client_id)
        if hasattr(client.channel, 'action'):
            action = client.channel.action.get_action()
            template = 'action/channel-auth.xml'
            context = {
                'client_id': client_id,
                'password': client.password,
                'verto_methods': action.verto_methods
            }
            return template, context
        raise Http404


register_directory_handler('verto', ChannelActionAuthHandler())
