""" Extension app URL config. """
from django.urls import path
from extension.views import IndexView, ClientView, SessionView


urlpatterns = [
    path(
        '',
        IndexView.as_view(),
        name='pbx-extension-index'
    ),
    path(
        '<uuid:channel_id>',
        ClientView.as_view(),
        name='pbx-extension-client'
    ),
    path(
        '<uuid:channel_id>/session',
        SessionView.as_view(),
        name='pbx-extension-session'
    ),
]
