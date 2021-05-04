""" Action app dialplan request handler module. """
from uuid import UUID
from django.db.utils import OperationalError
from django.http import Http404
from django.shortcuts import get_object_or_404
from dialplan.registries import DialplanHandler, register_dialplan_handler
from sofia.models import Extension, IntercomProfile
from verto.models import Client


class ActionHandler(DialplanHandler):
    """ Abstract dialplan request handler. """

    def get_action(self, request, context):
        """ Return an Action. """
        raise NotImplementedError

    def get_dialplan(self, request, context):
        """ Handle a dialplan request """
        action = self.get_action(request, context)
        template = action.get_template()
        context = {
            'context': context,
            'action': action
        }
        self.log_rendered(request, template, context)
        return template, context


class ClientActionHandler(ActionHandler):
    """ Handle a verto context dialplan request. """

    def get_action(self, request, context):
        """ Return a verto.models.Client's Action. """
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

        # Clients have a Channel and the caller puts channel_id in
        # Caller-Destination-Number. Do they match?
        channel_id = request.POST.get('Caller-Destination-Number')
        if not channel_id or channel_id != str(client.channel.channel_id):
            raise Http404

        # Actions have a Channel.
        if hasattr(client.channel, 'action'):
            return client.channel.action.get_action()
        raise Http404


class ExtensionActionHandler(ActionHandler):
    """ Handle an intercom context dialplan request. """

    def get_action(self, request, context):
        """ Return a sofia.models.Extension's action. """

        # Sofia puts the called number in Caller-Destination-Number.
        number = request.POST.get('Caller-Destination-Number')
        if not number:
            raise Http404
        extension = get_object_or_404(
            Extension,
            number=number,
            intercom__context=context
        )
        if not extension:
            raise Http404

        # Actions have an Extension.
        if hasattr(extension.channel, 'action'):
            return extension.channel.action.get_action()
        raise Http404


# These fail to load until tables exist.
try:
    register_dialplan_handler('verto', ClientActionHandler())
    for _intercom in IntercomProfile.objects.all():
        register_dialplan_handler(_intercom.domain, ExtensionActionHandler())
except OperationalError:
    pass
