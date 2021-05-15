""" Extension app admin module. """
from django.contrib import admin
from extension.models import Extension, MatchExtension


@admin.register(Extension)
class ExtensionAdmin(admin.ModelAdmin):
    """ Extension model admin tweaks. """


@admin.register(MatchExtension)
class MatchExtensionAdmin(admin.ModelAdmin):
    """ IntercomPattern model admin tweaks. """


class ActionAdmin(admin.ModelAdmin):
    """ An extension admin superclass. """
    exclude = ('channel',)
