""" Fsapi app URLs module. """
from django.urls import path
from fsapi import views


urlpatterns = [
    path('', views.FsapiView.as_view(), name='pbx-fsapi'),
]
