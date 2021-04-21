""" Fsapi app view module. """
import logging
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


def custom404(request):
    """ Custom 404 with 200 status code. """
    if request.POST.get('section') == 'configuration':
        logging.getLogger('django.server').info(
            'No handler for %s.', request.POST['key_value'],
        )
    else:
        logging.getLogger('django.server').info(
            'No handler for %s.', request.POST.dict()
        )
    return HttpResponse(render(request, 'fsapi/404.xml'))


@method_decorator(csrf_exempt, name='dispatch')
class FsapiView(View):
    """ Process API requests by passing the request to a registered
    fsapi request handler. """

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """ Handle API requests. """
        # pylint: disable=unused-argument
        request.custom404 = custom404
        try:
            for handler in settings.FSAPI_REQUEST_HANDLERS.registry:
                if handler.matches(request):
                    logging.getLogger('django.server').info(
                        'Processing %s', handler.__class__.__name__
                    )
                    template, context = handler.process(request)
                    return HttpResponse(render(request, template, context))
            raise Http404
        except (KeyError, ValueError) as err:
            raise SuspiciousOperation from err
