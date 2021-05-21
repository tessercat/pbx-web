""" Intercom app admin module. """
from django.contrib import admin
from intercom.models import (
    Extension, GatewayExtension,
    Bridge, Line, OutsideLine
)


@admin.register(Extension)
class ExtensionAdmin(admin.ModelAdmin):
    """ Extension model admin tweaks. """
    exclude = ('channel',)


@admin.register(GatewayExtension)
class GatewayExtensionAdmin(admin.ModelAdmin):
    """ GatewayExtension model admin tweaks. """


@admin.register(Bridge)
class BridgeAdmin(admin.ModelAdmin):
    """ Bridge model admin tweaks. """


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    """ Line model admin tweaks. """


@admin.register(OutsideLine)
class OutsideLineAdmin(admin.ModelAdmin):
    """ OutsideLine model admin tweaks. """
