""" Peers app URL config. """
from django.urls import path
from peers.views import ChannelView, SessionsView


urlpatterns = [
    path(
        '<uuid:channel_id>',
        ChannelView.as_view(),
        name='peers_channel'
    ),
    path(
        '<uuid:channel_id>/sessions',
        SessionsView.as_view(),
        name='peers_channel_sessions'
    ),
]
