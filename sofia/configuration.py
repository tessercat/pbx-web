""" Sofia app config request handler module. """
from django.shortcuts import get_object_or_404
from configuration.registries import (
    ConfigurationHandler,
    register_configuration_handler
)
from sofia.models import IntercomProfile  # , Gateway


class SofiaConfigHandler(ConfigurationHandler):
    """ Sofia profile config request handler. """

    def process(self, request):
        """ Return template/context. """
        # self.logger.info(request.POST.dict())
        profile = request.POST.get('profile')
        if profile:

            # Distinguish between gateway/intercom profile requests.
            # Add gateways.

            # Intercom profile request.
            obj = get_object_or_404(IntercomProfile, domain=profile)
            template = 'sofia/intercom.conf.xml'
            context = {
                'domain': obj.domain,
                'port': obj.port,
            }
            # self.log_rendered(request, template, context)
            return template, context

        # No profile specified in POST. Return all profiles.
        intercoms = []
        for obj in IntercomProfile.objects.all():
            intercoms.append({
                'domain': obj.domain,
                'port': obj.port,
            })
        template = 'sofia/sofia.conf.xml'
        context = {'intercoms': intercoms}
        # Add gateways to context.
        # self.log_rendered(request, template, context)
        return template, context


register_configuration_handler('sofia.conf', SofiaConfigHandler())
