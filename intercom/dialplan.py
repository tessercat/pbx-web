""" Intercom app dialplan request handler module. """
from uuid import UUID
from django.db.utils import OperationalError
from django.http import Http404
from django.shortcuts import get_object_or_404
from dialplan.registries import DialplanHandler, register_dialplan_handler
from intercom.models import Intercom, Extension
from verto.models import Client


class ExtensionDialplanHandler(DialplanHandler):
    """ Handle an Extension Action request. """

    def get_action(self, request, context):
        """ Return an Extension Action. """
        number = request.POST.get('Caller-Destination-Number')
        if not number:
            raise Http404
        try:

            # Match the number exactly.
            extension = Extension.objects.get(
                intercom__domain=context,
                number=number,
            )
        except Extension.DoesNotExist:

            # Match the number to an expression.
            extension = None
            extensions = Extension.objects.filter(
                intercom__domain=context,
                pcre=True,
            )
            for ext in extensions:
                if ext.matches(number):
                    extension = ext
                    break

        # Return the extension's Action.
        if hasattr(extension, 'action'):
            return extension.action.get_action()
        raise Http404


# These fail to load until tables exist.
try:
    for _intercom in Intercom.objects.all():
        register_dialplan_handler(
            _intercom.domain, ExtensionDialplanHandler()
        )
except OperationalError:
    pass


class ClientDialplanHandler(DialplanHandler):
    """ Handle a Client Action request. """

    def get_action(self, request, context):
        """ Return a Client's Action. """
        # pylint: disable=unused-argument

        # Get Client. Ignore destination number.
        client_id = request.POST.get('variable_user_name')
        if not client_id:
            raise Http404
        try:
            UUID(client_id, version=4)
        except (ValueError) as err:
            raise Http404 from err
        client = get_object_or_404(Client, client_id=client_id)

        # Return the Client's Channel's Extension's Action.
        if hasattr(client.channel, 'extension'):
            extension = client.channel.extension

            # And Actions have an Extension field.
            if hasattr(extension, 'action'):
                return extension.action.get_action()
        raise Http404


register_dialplan_handler('verto', ClientDialplanHandler())
