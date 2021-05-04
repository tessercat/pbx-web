""" Action app URL config. """
from django.urls import path
from action.views import IndexView, ClientView, SessionView


urlpatterns = [
    path(
        '',
        IndexView.as_view(),
        name='pbx-action-index'
    ),
    path(
        '<uuid:channel_id>',
        ClientView.as_view(),
        name='pbx-action-client'
    ),
    path(
        '<uuid:channel_id>/session',
        SessionView.as_view(),
        name='pbx-action-session'
    ),
]
