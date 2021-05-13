""" Sofia app config request handler module. """
from django.conf import settings
from django.shortcuts import get_object_or_404
from configuration.registries import (
    ConfigurationHandler,
    register_configuration_handler
)
from sofia.models import IntercomProfile, GatewayProfile


class SofiaConfigHandler(ConfigurationHandler):
    """ Sofia profile config request handler. """

    def process(self, request):
        """ Return template/context to configure mod_sofia. """
        # self.logger.info(request.POST.dict())
        domain = request.POST.get('profile')
        if domain:

            # The profile thread has requested its own configuration.
            try:
                intercom = IntercomProfile.objects.get(domain=domain)
                template = 'sofia/intercom.conf.xml'
                context = {'intercom': intercom}
            except IntercomProfile.DoesNotExist:
                gateway = get_object_or_404(GatewayProfile, domain=domain)
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
            'intercoms': IntercomProfile.objects.all(),
            'gateways': GatewayProfile.objects.all()
        }
        # self.log_rendered(request, template, context)
        return template, context


register_configuration_handler('sofia.conf', SofiaConfigHandler())
