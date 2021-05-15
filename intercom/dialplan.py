""" Intercom app dialplan request handler module. """
from django.db.utils import OperationalError
from django.http import Http404
from dialplan.registries import register_dialplan_handler
from extension.dialplan import ExtensionHandler
from extension.models import Extension, MatchExtension
from intercom.models import Intercom


class IntercomHandler(ExtensionHandler):
    """ Handle an intercom context dialplan request. """

    def get_extension(self, request, context):
        """ Return an IntercomExtension. """
        number = request.POST.get('Caller-Destination-Number')
        if not number:
            raise Http404
        try:

            # Match the number exactly.
            obj = Extension.objects.get(
                number=number,
                intercom__domain=context
            )
        except Extension.DoesNotExist as err:

            # Match the number to a pattern.
            patterns = MatchExtension.objects.filter(
                intercom__domain=context
            )
            obj = None
            for pattern in patterns:
                if pattern.matches(number):
                    obj = pattern
                    break
            if not obj:
                raise Http404 from err

        # Return the extension.
        if getattr(obj, 'extension'):
            return obj.extension.get_extension()
        raise Http404


# These fail to load until tables exist.
try:
    for _intercom in Intercom.objects.all():
        register_dialplan_handler(_intercom.domain, IntercomHandler())
except OperationalError:
    pass
