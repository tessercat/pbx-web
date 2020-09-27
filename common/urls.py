""" Channels app URL config. """
from django.urls import path
from common.views import AboutView


urlpatterns = [
    path('about', AboutView.as_view(), name='about'),
]
