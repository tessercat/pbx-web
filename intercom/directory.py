""" Intercom app directory request handler module. """
from uuid import UUID
from django.http import Http404
from django.shortcuts import get_object_or_404
from directory.registries import DirectoryHandler, register_directory_handler
from verto.models import Client


class ClientAuthHandler(DirectoryHandler):
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
        if hasattr(client.channel, 'extension'):
            template = 'intercom/client-auth.xml'
            context = {
                'client_id': client_id,
                'password': client.password,
            }
            return template, context
        raise Http404


register_directory_handler('verto', ClientAuthHandler())
""" Sofia app directory request handler module. """
from django.db.utils import OperationalError
from django.http import Http404
from django.shortcuts import get_object_or_404
from directory.registries import DirectoryHandler, register_directory_handler
from intercom.models import Intercom, Line


class LineAuthHandler(DirectoryHandler):
    """ Handle Line auth requests. """

    def get_directory(self, request, domain):
        """ Return template/context to auth a Line registration. """

        # Reject directory gateway requests.
        purpose = request.POST.get('purpose')
        if purpose and purpose == 'gateways':
            # 1.10.6 does this when <domain> is configured and parse=false.
            raise Http404

        # Send the line-auth template.
        intercom = get_object_or_404(Intercom, domain=domain)
        user = request.POST.get('user')
        if not user:
            raise Http404
        line = get_object_or_404(Line, username=user, intercom=intercom)
        template = 'intercom/line-auth.xml'
        context = {
            'domain': domain,
            'user_id': user,
            'password': line.password
        }
        return template, context


# These don't load until tables exist.
try:
    for _intercom in Intercom.objects.all():
        register_directory_handler(_intercom.domain, LineAuthHandler())
except OperationalError:
    pass
