""" Dialplan registries module. """
import logging
from fsapi.registries import Handler


dialplan_handler_registry = {}


class DialplanHandler(Handler):
    """ Abstract dialplan handler. """

    def get_action(self, request, context):
        """ Return an Action object. """
        raise NotImplementedError

    def get_dialplan(self, request, context):
        """ Return a template/context. """
        action = self.get_action(request, context)
        template = action.template
        context = {
            'context': context,
            'action': action,
        }
        self.log_rendered(request, template, context)
        return template, context


def register_dialplan_handler(context, handler):
    """ Add a dialplan handler to the registry."""
    dialplan_handler_registry[context] = handler
    logging.getLogger('django.server').info(
        'dialplan %s %s', handler.__class__.__name__, context
    )
