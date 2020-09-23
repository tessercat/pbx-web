""" FsAPI request handler module. """
import logging
from django.conf import settings
from django.shortcuts import render


class RequestHandler:
    """ Request handler abstract class. Apps that handle FsApi requests
    add custom RequestHandlers to the project settings handler registry
    in the app's fsapi module. """

    logger = logging.getLogger('django.server')
    admin_logger = logging.getLogger('django.pbx')

    def __init__(self, **kwargs):
        """ Initialize expected key/value pairs. """
        self.keys = {
            'hostname': settings.PBX_HOSTNAME,
        }
        self.keys.update(**kwargs)

    def log_rendered(self, request, template, context):
        """ Log the template as rendered in the context. Use this in
        implementations of the process method to debug templates. """
        self.logger.info(render(request, template, context).content.decode())

    def matches(self, request):
        """ Return True if request POST data contains all expected key/value
        pairs. """
        for key in self.keys:
            if (
                    key not in request.POST
                    or self.keys[key] != request.POST[key]):
                return False
        return True

    def process(self, request):
        """ Process the request and raise django.http.Http404 or ValueError if
        request POST data can't be processed, or return a tuple of template and
        context if it can. """
        raise NotImplementedError


class RequestHandlerRegistry:
    """ FsApi request handler registry. """
    # pylint: disable=too-few-public-methods

    _registry = []
    registry = _registry


fsapi_request_handler_registry = RequestHandlerRegistry()


def register_handlers(*args):
    """ Add handlers to the global handler registry."""
    for handler in args:
        fsapi_request_handler_registry.registry.append(handler)
        logging.getLogger('django.server').info(
            'Registered %s', handler.__class__.__name__
        )
