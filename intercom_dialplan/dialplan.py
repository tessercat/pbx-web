""" Intercom dialplan app dialplan request handler module. """
from uuid import UUID
from django.db.utils import OperationalError
from django.http import Http404
from django.shortcuts import get_object_or_404
from dialplan.registries import DialplanHandler, register_dialplan_handler
from intercom.models import Intercom, Line
from intercom_dialplan.apps import intercom_dialplan_settings
from intercom_dialplan.models import Extension, OutboundCallMatcher
from verto.models import Client


class ActionHandler(DialplanHandler):
    """ Handle Line/Client extension action requets. """

    @staticmethod
    def get_action(extension):
        """ Return extension action. """
        if hasattr(extension, 'intercomaction'):
            for name in intercom_dialplan_settings['action_names']:
                if hasattr(extension.intercomaction, name):
                    return getattr(extension.intercomaction, name)
        raise Http404

    def get_dialplan(self, request, domain):
        """ Return a template/context. """
        raise NotImplementedError


class LineCallHandler(ActionHandler):
    """ Line call dialplan request handler. """

    matchers = None

    def get_matchers(self):
        """ Return cached matchers or set and send. """
        if not self.matchers:
            self.matchers = OutboundCallMatcher.objects.all()
        return self.matchers

    # Handle 404 with an annotation.
    def get_dialplan(self, request, domain):
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
                intercom__domain=domain,
                extension_number=number
            )
            action = self.get_action(extension)
            template = action.template
            context = {
                'line': line,
                'extension': extension,
                'action': action
            }
            self.log_rendered(request, template, context)
            return template, context
        except Extension.DoesNotExist:
            for matcher in self.get_matchers():
                if matcher.matches(number):
                    template = matcher.template
                    context = {
                        'line': line,
                        'matcher': matcher
                    }
                    self.log_rendered(request, template, context)
                    return template, context

        # No action and no match.
        raise Http404


# These fail to load until tables exist.
try:
    for _intercom in Intercom.objects.all():
        register_dialplan_handler(_intercom.domain, LineCallHandler())
except OperationalError:
    pass


class ClientCallHandler(ActionHandler):
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
    def get_dialplan(self, request, domain):
        """ Return Client Extension template/context. """
        # pylint: disable=unused-argument
        client = self.get_client(request)
        if not hasattr(client.channel, 'extension'):
            raise Http404
        extension = client.channel.extension
        action = self.get_action(extension)
        template = action.template
        context = {
            'client': client,
            'extension': extension,
            'action': action
        }
        # self.log_rendered(request, template, context)
        return template, context


register_dialplan_handler('verto', ClientCallHandler())
