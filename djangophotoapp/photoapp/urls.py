from django.conf.urls import url
from photoapp import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^signin$', views.SigninView.as_view(), name='signin'),
]
