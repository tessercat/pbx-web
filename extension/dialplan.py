""" Extension app dialplan request handler module. """
from uuid import UUID
from django.http import Http404
from django.shortcuts import get_object_or_404
from dialplan.registries import DialplanHandler, register_dialplan_handler
from verto.models import Client


class ExtensionHandler(DialplanHandler):
    """ Abstract dialplan extension handler. """

    def get_extension(self, request, context):
        """ Return an extension object. """
        raise NotImplementedError

    def get_dialplan(self, request, context):
        """ Handle a dialplan request """
        extension = self.get_extension(request, context)
        template = extension.get_template()
        context = {
            'context': context,
            'extension': extension,
        }
        self.log_rendered(request, template, context)
        return template, context


class ClientExtensionHandler(ExtensionHandler):
    """ Handle a verto context dialplan request. """

    def get_extension(self, request, context):
        """ Return a Client's Extension. """
        # pylint: disable=unused-argument

        # Verto puts client_id in variable_user_name.
        client_id = request.POST.get('variable_user_name')
        if not client_id:
            raise Http404
        try:
            UUID(client_id, version=4)
        except (ValueError) as err:
            raise Http404 from err
        client = get_object_or_404(Client, client_id=client_id)

        # Extensions have a Channel reference.
        if hasattr(client.channel, 'extension'):
            return client.channel.extension.get_extension()
        raise Http404


register_dialplan_handler('verto', ClientExtensionHandler())
