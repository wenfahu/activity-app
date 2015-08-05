from django.conf.urls import patterns, include, url
from act.views_activity import *
from act.views_user import *

urlpatterns = patterns('',
    url(r'^register/$', register, name = 'register'),
    url(r'^login/$', user_login, name = 'login'),
    url(r'^user/(?P<user_name>[0-9a-zA-Z@_\.-]+)/request$', request_user_info, name = 'request_userinfo'),
    url(r'^user/(?P<user_name>[0-9a-zA-Z@_\.-]+)/page$', request_user_page, name = 'request_user_page'),
    url(r'^user/(?P<user_name>[0-9a-zA-Z@_\.-]+)/update$', update_user, name = "update_user"),
    url(r'^user/requestAll$', get_user_list, name = "get_user_list"),
    url(r'^activity/create$', create_activity, name = "create_activity"),
    url(r'^activity/(?P<SID>[0-9a-zA-z@_\.-]+)/request$', get_activity, name = "get_activity"),
    url(r'^activity/(?P<SID>[0-9a-zA-z@_\.-]+)/join$', participate_activity, name = "participate_activity"),
    url(r'^activity/(?P<SID>[0-9a-zA-z@_\.-]+)/quit$', quit_activity, name = "quit_activity"),
    url(r'^activity/requestAll$', get_activity_list, name = "get_activity_list"),
)
