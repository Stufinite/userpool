from django.http import HttpResponse, JsonResponse

from django.contrib.auth.models import User

from django.views.decorators.cache import never_cache

import pylibmc
memcache_client = pylibmc.Client(['127.0.0.1:11211'])


@never_cache
def get_user(request, session_id=''):
    session_key = request.session.session_key if session_id == '' else session_id
    if session_key == None or memcache_client.get(':1:django.contrib.sessions.cache' + session_key) == None:
        return HttpResponse('None')
    else:
        uid = memcache_client.get(
            ':1:django.contrib.sessions.cache' + session_key)['_auth_user_id']
        user = User.objects.get(pk=uid)
        user_dict = {
            'username': user.username,
            'email': user.email,
            'name': user.first_name + ' ' + user.last_name,
            'grade': user.userprofile.grade,
            'major': user.userprofile.major,
            'second_major': user.userprofile.second_major,
            'career': user.userprofile.career,
        }
        return JsonResponse(user_dict)


@never_cache
def get_username(request, session_id=''):
    session_key = request.session.session_key if session_id == '' else session_id
    if session_key == None or memcache_client.get(':1:django.contrib.sessions.cache' + session_key) == None:
        return HttpResponse('None')
    else:
        uid = memcache_client.get(
            ':1:django.contrib.sessions.cache' + session_key)['_auth_user_id']
        user = User.objects.get(pk=uid)
        return HttpResponse(user.username)
