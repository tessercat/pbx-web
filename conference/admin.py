""" Conference app admin module. """
from django.contrib import admin
from conference.models import Conference
from action.admin import ActionAdmin


@admin.register(Conference)
class ConferenceAdmin(ActionAdmin):
    """ Conference model admin tweaks. """
