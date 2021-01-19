""" Peers app URL config. """
from django.urls import path
from peers.views import AboutView, PeerView, PublicView, SessionView


urlpatterns = [
    path(
        '',
        PublicView.as_view(),
        name='peers_public'
    ),
    path(
        'about',
        AboutView.as_view(),
        name='peers_about'
    ),
    path(
        'peers/<uuid:channel_id>',
        PeerView.as_view(),
        name='peers_channel'
    ),
    path(
        'peers/<uuid:channel_id>/session',
        SessionView.as_view(),
        name='peers_session'
    ),
]
