""" Conference app configuration request handler module. """
from django.conf import settings
from configuration.fsapi import ModConfigHandler, register_mod_handler
)


class ConferenceConfigHandler(ConfigurationHandler):
    """ Conference module config request handler. """

    def process(self, request):
        """ Return template/context. """
        template = 'conference/conference.conf.xml'
        context = {
            'domain': settings.PBX_HOSTNAME,
        }
        return template, context


register_configuration_handler('conference.conf', ConferenceConfigHandler())
