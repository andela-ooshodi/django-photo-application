from django.conf.urls import include, url
from django.contrib import admin
import photoapp.views
import photoapp.urls

urlpatterns = [
    url(r'^', include(photoapp.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
]


handler404 = 'photoapp.views.custom404'
handler500 = 'photoapp.views.custom500'
