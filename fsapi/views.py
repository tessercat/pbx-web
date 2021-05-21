""" Fsapi app view module. """
import logging
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


def custom404(request):
    """ Custom 404 with 200 status code. """
    return HttpResponse(render(request, 'fsapi/404.xml'))


fsapi_handlers = []


def register_fsapi_handler(handler):
    """ Add a handler to the global handler registry."""
    fsapi_handlers.append(handler)
    logging.getLogger('django.server').info('fsapi %s', handler)


class Handler:
    """ Base handler with loggers. """
    # pylint: disable=too-few-public-methods

    logger = logging.getLogger('django.server')
    admin_logger = logging.getLogger('django.pbx')

    def log_rendered(self, request, template, context):
        """ Log the template as rendered in the context. """
        self.logger.info(render(request, template, context).content.decode())

    def __str__(self):
        return self.__class__.__name__


class FsapiHandler(Handler):
    """ Handle requests based on POST field matches. """

    def __init__(self, **kwargs):
        """ Initialize expected key/value pairs. """
        self.keys = {
            'hostname': settings.PBX_HOSTNAME,
        }
        self.keys.update(**kwargs)

    def matches(self, request):
        """ Return True if POST data contains all expected keys/values. """
        for key in self.keys:
            if (
                    key not in request.POST
                    or self.keys[key] != request.POST[key]):
                return False
        return True

    def process(self, request):
        """ Return template/context. """
        raise NotImplementedError


@method_decorator(csrf_exempt, name='dispatch')
class FsapiView(View):
    """ Process API requests by passing the request to a registered
    fsapi request handler. """

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """ Handle API requests. """
        # pylint: disable=unused-argument
        request.custom404 = custom404
        for handler in fsapi_handlers:
            if handler.matches(request):
                template, context = handler.process(request)
                return HttpResponse(render(request, template, context))
        raise Http404
