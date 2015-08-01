from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^register/$', views.register, name = 'register'),
    url(r'^login/$', views.user_login, name = 'login'),
    url(r'^user/(?P<user_name>[0-9a-zA-Z@_\.-]+)$', views.request_user_info, name = 'request_userinfo'),
    url(r'^user/(?P<user_name>[0-9a-zA-Z@_\.-]+)/update$', views.update_user, name = "update_user"),
)
