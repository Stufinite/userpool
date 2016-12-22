from django.conf.urls import url

from .views import views, apis

# Views that related with user creation and authentication
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/forgot/$', views.forgot_password, name='forgot'),
    url(r'^accounts/verify/$', views.verify, name='verify'),
    url(r'^accounts/verify/resend$', views.reverify, name='reverify'),
]

# Views that related with user profile
urlpatterns += [
    url(r'^accounts/profile/$', views.profile_info, name='profile'),
    url(r'^accounts/profile/password$', views.profile_password, name='password'),
    url(r'^accounts/profile/edit$', views.profile_edit, name='edit'),
]

# User retrieve API
urlpatterns += [
    url(r'^control_api/session_key/$', apis.get_session_key),
    url(r'^auth/get_user/$', apis.get_user),
    url(r'^auth/get_user/(?P<session_id>\w*)$', apis.get_user),
]
