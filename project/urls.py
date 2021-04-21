""" Project URL Configuration """
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from common.views import custom400
from common.views import custom404
from conference.views import IndexView


admin.site.site_header = 'PBX'
admin.site.site_title = 'PBX'

handler400 = custom400
handler404 = custom404

urlpatterns = [
    path('', include('django_prometheus.urls')),
    path('', IndexView.as_view(), name='pbx-conference-index'),
    path('fsapi', include('fsapi.urls')),
    path('%s/' % settings.CONFERENCE_REALM, include('conference.urls')),
    path('admin/', admin.site.urls),
]
