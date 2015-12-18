from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
import photoapp.views
import photoapp.urls

urlpatterns = [
    url(r'^', include(photoapp.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    })
]


handler404 = 'photoapp.views.custom404'
handler500 = 'photoapp.views.custom500'
