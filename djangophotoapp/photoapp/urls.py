from django.conf.urls import url
from photoapp import views

urlpatterns = [
    url(r'^home$', views.HomeView.as_view(), name='home'),
    url(r'^$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    url(r'^filter$', views.FilterView.as_view(), name='filter'),
]
