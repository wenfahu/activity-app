from django.conf.urls import patterns, include, url
from act.views_activity import *
from act.views_user import *

urlpatterns = patterns('',
    url(r'^register/$', register, name = 'register'),
    url(r'^login/$', user_login, name = 'login'),
    url(r'^user/(?P<user_name>[0-9a-zA-Z@_\.-]+)$', request_user_info, name = 'request_userinfo'),
    url(r'^user/(?P<user_name>[0-9a-zA-Z@_\.-]+)/update$', update_user, name = "update_user"),
)
