""" Sofia app directory request handler module. """
from django.db.utils import OperationalError
from django.http import Http404
from django.shortcuts import get_object_or_404
from directory.registries import DirectoryHandler, register_directory_handler
from sofia.models import IntercomProfile, IntercomLine


class IntercomAuthHandler(DirectoryHandler):
    """ Intercom profile directory request handler. """

    def get_directory(self, request, domain):
        """ Return template/context to auth an IntercomLine registration. """

        # Reject directory gateway requests.
        purpose = request.POST.get('purpose')
        if purpose and purpose == 'gateways':
            # 1.10.6 does this <domain> is configured, even when parse=false.
            raise Http404

        # Send the line-auth template.
        intercom = get_object_or_404(IntercomProfile, domain=domain)
        user = request.POST.get('user')
        if not user:
            raise Http404
        line = get_object_or_404(
            IntercomLine, username=user, intercom=intercom
        )
        template = 'sofia/line-auth.xml'
        context = {
            'domain': domain,
            'user_id': user,
            'password': line.password
        }
        return template, context


# These don't load until tables exist.
try:
    for _intercom in IntercomProfile.objects.all():
        register_directory_handler(_intercom.domain, IntercomAuthHandler())
except OperationalError:
    pass
