""" Channels app URL config. """
from django.urls import path
from channels.views import IndexView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
