from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^register/$', views.register, name = 'register'),
    url(r'^login/$', views.user_login, name = 'login'),
    url(r'^request_user_info/$', views.request_user_info, name = 'request_user_info'),
)
