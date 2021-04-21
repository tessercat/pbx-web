""" Conference app fsapi request handler module. """
from django.conf import settings
from fsapi.registries import FsapiHandler, register_fsapi_handler


class ConferenceConfigHandler(FsapiHandler):
    """ Conference module config request handler. """

    def __init__(self):
        super().__init__(
            key_value='conference.conf',
            section='configuration',
        )

    def process(self, request):
        """ Process conference configuration requests. """
        template = 'conference/conference.conf.xml'
        context = {
            'domain': settings.PBX_HOSTNAME,
        }
        return template, context


register_fsapi_handler(ConferenceConfigHandler())
