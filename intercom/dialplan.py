""" Intercom dialplan app dialplan request handler module. """
from uuid import UUID
from django.db.utils import OperationalError
from django.http import Http404
from django.shortcuts import get_object_or_404
from dialplan.fsapi import DialplanHandler, register_dialplan_handler
from intercom.models import (
    Intercom, Gateway,
    Extension, GatewayExtension,
    Line, OutsideLine
)
from verto.models import Client


class LineCallHandler(DialplanHandler):
    """ Line call dialplan request handler. """

    # Handle 404 with an annotation.
    def get_dialplan(self, request, context):
        """ Return Line Extension/Matcher template/context. """

        # Get the dialed number.
        number = request.POST.get('Caller-Destination-Number')
        if not number:
            raise Http404

        # Get the calling Line.
        username = request.POST.get('variable_user_name')
        if not username:
            raise Http404
        line = get_object_or_404(Line, username=username)

        # Handle action or matcher
        try:
            extension = Extension.objects.get(
                intercom__domain=context,
                extension_number=number
            )
            action = extension.get_action()
            if not action:
                raise Http404
            template = action.template
            template_context = {
                'line': line,
                'extension': extension,
                'action': action
            }
            self.log_rendered(request, template, template_context)
            return template, template_context
        except Extension.DoesNotExist:
            extensions = GatewayExtension.objects.all()
            for extension in extensions:
                if extension.matches(number):
                    template = extension.template
                    template_context = {
                        'line': line,
                        'extension': extension
                    }
                    self.log_rendered(request, template, template_context)
                    return template, template_context

        # No action and no match.
        raise Http404


# These fail to load until tables exist.
try:
    for _intercom in Intercom.objects.all():
        register_dialplan_handler(_intercom.domain, LineCallHandler())
except OperationalError:
    pass


class ClientCallHandler(DialplanHandler):
    """ Client dialplan request handler. """

    @staticmethod
    def get_client(request):
        """ Return the calling Client. """
        client_id = request.POST.get('variable_user_name')
        if not client_id:
            raise Http404
        try:
            UUID(client_id, version=4)
        except (ValueError) as err:
            raise Http404 from err
        # Validate that the client session has not expired?
        return get_object_or_404(Client, client_id=client_id)

    # Handle 404 with an annotation.
    def get_dialplan(self, request, context):
        """ Return Client Extension template/context. """
        # pylint: disable=unused-argument
        client = self.get_client(request)
        if not hasattr(client.channel, 'extension'):
            raise Http404
        extension = client.channel.extension
        action = extension.get_action(extension)
        if not action:
            raise Http404
        template = action.template
        template_context = {
            'client': client,
            'extension': extension,
            'action': action
        }
        # self.log_rendered(request, template, template_context)
        return template, template_context


register_dialplan_handler('verto', ClientCallHandler())


class GatewayCallHandler(DialplanHandler):
    """ Gateway inbound call dialplan request handler. """

    # Handle 404 with an annotation.
    def get_dialplan(self, request, context):
        """ Return template/context. """
        number = request.POST.get('Caller-Destination-Number')
        if not number:
            raise Http404
        transfer = get_object_or_404(
            InboundTransfer,
            number=number,
        )
        template = transfer.template
        template_context = {'extension': transfer.extension}
        self.log_rendered(request, template, template_context)
        return template, template_context


# These fail to load until tables exist.
try:
    for _gateway in Gateway.objects.all():
        register_dialplan_handler(_gateway.domain, GatewayCallHandler())
except OperationalError:
    pass
