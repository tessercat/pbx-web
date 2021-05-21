""" Sofia app config request handler module. """
from django.conf import settings
from django.shortcuts import get_object_or_404
from configuration.fsapi import ModConfigHandler, register_mod_handler
from sofia.models import Intercom, Gateway


class SofiaConfigHandler(ModConfigHandler):
    """ Sofia profile config request handler. """

    def get_config(self, request):
        """ Return template/context to configure mod_sofia. """
        # self.logger.info(request.POST.dict())
        domain = request.POST.get('profile')
        if domain:

            # The profile thread has requested its own configuration.
            try:
                intercom = Intercom.objects.get(domain=domain)
                template = 'sofia/intercom.conf.xml'
                context = {'intercom': intercom}
            except Intercom.DoesNotExist:
                gateway = get_object_or_404(Gateway, domain=domain)
                template = 'sofia/gateway.conf.xml'
                context = {
                    'gateway': gateway,
                    'hostname': settings.PBX_HOSTNAME
                }
            # self.log_rendered(request, template, context)
            return template, context

        # No profile specified in POST. Return all profiles.
        template = 'sofia/sofia.conf.xml'
        context = {
            'intercoms': Intercom.objects.all(),
            'gateways': Gateway.objects.all()
        }
        # self.log_rendered(request, template, context)
        return template, context


register_mod_handler('sofia', SofiaConfigHandler())
