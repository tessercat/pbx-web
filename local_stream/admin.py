""" Local stream app admin module. """
from django.contrib import admin
from local_stream.models import Playback, Recording
from action.admin import ActionAdmin


@admin.register(Playback)
class PlaybackAdmin(ActionAdmin):
    """ Playback model admin tweaks. """


@admin.register(Recording)
class RecordingAdmin(ActionAdmin):
    """ Recording model admin tweaks. """
