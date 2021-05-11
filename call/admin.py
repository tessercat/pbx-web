""" Call app admin module. """
from django.contrib import admin
from call.models import Call
from action.admin import ActionAdmin


@admin.register(Call)
class CallAdmin(ActionAdmin):
    """ Call model admin tweaks. """
    list_display = ('name', 'extension', 'line', 'channel_repr')
