""" Channels app URL config. """
from django.urls import path
from channels.views import AboutView, IndexView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about', AboutView.as_view(), name='about'),
]
