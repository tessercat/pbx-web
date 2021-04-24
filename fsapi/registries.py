""" Fsapi registries module. """
import logging
from django.conf import settings
from django.shortcuts import render


class Handler:
    """ Base handler with loggers. """
    # pylint: disable=too-few-public-methods

    logger = logging.getLogger('django.server')
    admin_logger = logging.getLogger('django.pbx')

    def log_rendered(self, request, template, context):
        """ Log the template as rendered in the context. """
        self.logger.info(render(request, template, context).content.decode())


fsapi_handler_registry = []


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
        """ Return a tuple of template and context. """
        raise NotImplementedError


def register_fsapi_handler(handler):
    """ Add a handler to the global handler registry."""
    fsapi_handler_registry.append(handler)
    logging.getLogger('django.server').info(
        'Registered fsapi handler %s', handler.__class__.__name__
    )
