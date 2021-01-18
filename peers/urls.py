""" Peers app URL config. """
from django.urls import path
from peers.views import AboutView, IndexView, PeerView, SessionView


urlpatterns = [
    path(
        '',
        IndexView.as_view(),
        name='peers_index'
    ),
    path(
        'about',
        AboutView.as_view(),
        name='peers_about'
    ),
    path(
        '<uuid:channel_id>',
        PeerView.as_view(),
        name='peers_channel'
    ),
    path(
        '<uuid:channel_id>/session',
        SessionView.as_view(),
        name='peers_session'
    ),
]
