""" FsApi app URLs module. """
from django.urls import path
from fsapi import views


urlpatterns = [
    path('', views.FsApiView.as_view()),
]
