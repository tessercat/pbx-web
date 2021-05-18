""" Intercom app dialplan request handler module. """
from uuid import UUID
from django.db.utils import OperationalError
from django.http import Http404
from django.shortcuts import get_object_or_404
from dialplan.registries import DialplanHandler, register_dialplan_handler
from intercom.apps import intercom_settings
from intercom.models import Intercom, Extension, Line
from verto.models import Client


class IntercomDialplanHandler(DialplanHandler):
    """ Abstract intercom dialplan handler. """

    def get_caller(self, request):
        """ Return a caller object. """
        raise NotImplementedError

    def get_extension(self, request, context, caller):
        """ Return an Extension object. """
        raise NotImplementedError

    def get_dialplan(self, request, context):
        """ Return a template/context. """
        caller = self.get_caller(request)
        extension = self.get_extension(request, context, caller)

        # Get the Extension's action.
        action = None
        if hasattr(extension, 'intercomaction'):
            for name in intercom_settings['action_names']:
                if hasattr(extension.intercomaction, name):
                    action = getattr(extension.intercomaction, name)
                    break
        if not action:
            raise Http404

        # Return template/context.
        template = action.template
        context = {
            'context': context,
            'extension': extension,
            'action': action,
            'caller': caller
        }
        # self.log_rendered(request, template, context)
        return template, context


class LineDialplanHandler(IntercomDialplanHandler):
    """ Line dialplan request handler. """

    def get_caller(self, request):
        """ Return the calling Line. """
        username = request.POST.get('variable_user_name')
        if username:
            try:
                line = Line.objects.get(username=username)
                return line.name
            except Line.DoesNotExist:
                return username
        raise Http404

    def get_extension(self, request, context, caller):
        """ Return a Line call's Extension. """
        number = request.POST.get('Caller-Destination-Number')
        if not number:
            raise Http404
        try:

            # Match the number exactly.
            return Extension.objects.get(
                intercom__domain=context,
                extension_number=number,
            )
        except Extension.DoesNotExist:

            # Match the number to an expression.
            extensions = Extension.objects.filter(
                intercom__domain=context,
                pcre_match=True,
            )
            for extension in extensions:
                if extension.matches(number):
                    return extension

        # No match. Failover extension?
        raise Http404


# These fail to load until tables exist.
try:
    for _intercom in Intercom.objects.all():
        register_dialplan_handler(_intercom.domain, LineDialplanHandler())
except OperationalError:
    pass


class ClientDialplanHandler(IntercomDialplanHandler):
    """ Client dialplan request handler. """

    def get_caller(self, request):
        """ Return the calling Client. """
        client_id = request.POST.get('variable_user_name')
        if not client_id:
            raise Http404
        try:
            UUID(client_id, version=4)
        except (ValueError) as err:
            raise Http404 from err
        return get_object_or_404(Client, client_id=client_id)

    def get_extension(self, request, context, caller):
        """ Return a Client call's Extension. """
        # pylint: disable=unused-argument
        if hasattr(caller.channel, 'extension'):
            return caller.channel.extension
        raise Http404


register_dialplan_handler('verto', ClientDialplanHandler())
