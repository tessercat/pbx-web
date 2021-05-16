""" Action app dialplan request handler module. """
from dialplan.registries import DialplanHandler


class ActionHandler(DialplanHandler):
    """ Abstract generic dialplan action handler. """

    def get_action(self, request, context):
        """ Return an extension object. """
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
