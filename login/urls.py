from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views

# Views that related with user creation and authentication
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout,
        {'template_name': 'logout.html'}, name='logout'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/forgot/$', views.forgot_password, name='forgot'),
]

# Views that related with user profile
urlpatterns += [
    url(r'^accounts/profile/$', views.profile_info, name='profile'),
    url(r'^accounts/profile/password$', views.profile_password, name='password'),
    url(r'^accounts/profile/edit$', views.profile_edit, name='edit'),
]


urlpatterns += [
    url(r'^accounts/verify/$', views.verify, name='verify'),
]
