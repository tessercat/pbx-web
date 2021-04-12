""" Conference app URL config. """
from django.urls import path
from conference.views import IndexView, ClientView, SessionView


urlpatterns = [
    path(
        '',
        IndexView.as_view(),
        name='pbx-conference-index'
    ),
    path(
        '<uuid:channel_id>',
        ClientView.as_view(),
        name='pbx-conference-client'
    ),
    path(
        '<uuid:channel_id>/session',
        SessionView.as_view(),
        name='pbx-conference-session'
    ),
]
