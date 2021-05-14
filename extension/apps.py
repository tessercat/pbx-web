""" Extension app config module. """
from django.apps import AppConfig


extension_settings = {}


class ExtensionConfig(AppConfig):
    """ Extension app config. """
    name = 'extension'

    def ready(self):
        """ Init app on ready. """
        # pylint: disable=import-outside-toplevel
        import logging
        from django.db.models import signals
        from extension.models import (
            Extension, post_save_handler, post_delete_handler
        )

        # Configure action_names.
        extension_names = []
        for extension in Extension.__subclasses__():
            signals.post_save.connect(post_save_handler, extension)
            signals.post_delete.connect(post_delete_handler, extension)
            extension_names.append(extension._meta.model_name)
        extension_settings['extension_names'] = extension_names
        logging.getLogger('django.server').info(
            '%s subclasses %s', self.name, ' '.join(extension_names)
        )
