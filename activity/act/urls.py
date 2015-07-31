from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^register/$', views.register, name = 'register'),
    url(r'^login/$', views.user_login, name = 'login'),
    url(r'^user/([0-9a-zA-Z@.+-_]+)$', views.request_user_info, name = 'request_userinfo'),
    url(r'^update_user_info/([0-9a-zA-Z@.+-_]+)$', views.update_user_info, name = 'update_userinfo'),
)
