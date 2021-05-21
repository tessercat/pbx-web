""" Verto app config request handler module. """
from django.conf import settings
from configuration.fsapi import ModConfigHandler, register_mod_handler


class VertoConfigHandler(ModConfigHandler):
    """ Verto config request handler. """

    def get_config(self, request):
        """ Return template/context. """
        template = 'verto/verto.conf.xml'
        context = {'port': settings.PORTS['verto']}
        return template, context


register_mod_handler('verto', VertoConfigHandler())
