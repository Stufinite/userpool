from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse

from django.views.decorators.cache import never_cache

from login.models import FacebookUser
from userpool.settings import UNIVERSAL_URL as UNIVERSAL_URL
from userpool.settings import FB_APP_ID as FB_APP_ID
from userpool.settings import FB_APP_SEC as FB_APP_SEC

import requests
import json
import redis


def get_user_id(key):
    rc = redis.StrictRedis(host='localhost', port=6379, db=0)
    return rc.get(key)


def set_user_id(key, val):
    rc = redis.StrictRedis(host='localhost', port=6379, db=0)
    return rc.set(key, val)


def del_user_id(key):
    rc = redis.StrictRedis(host='localhost', port=6379, db=0)
    return rc.delete(key)


@never_cache
def user_login(request):
    redirect_service = request.GET.get('redirect_service')
    client_id = "client_id=" + FB_APP_ID
    client_sec = "&client_secret=" + FB_APP_ID

    if not request.session.session_key:
        request.session.save()
    if get_user_id(request.session.session_key) == None:
        # Register or Login
        redirect_uri = "&redirect_uri=" + \
            UNIVERSAL_URL.format('login') + "/fb?redirect_service=" + redirect_service
        code = "&code=" + str(request.GET.get('code'))

        # get user access token
        url_user_token = "https://graph.facebook.com/v2.9/oauth/access_token?" + \
            client_id + client_sec + redirect_uri + code
        user_token = "input_token=" + \
            json.loads(requests.get(url_user_token).text)['access_token']

        # get app access token
        url_access_token = "https://graph.facebook.com/v2.9/oauth/access_token?" + \
            client_id + client_sec + "&grant_type=client_credentials"
        access_token = "&access_token=" + \
            json.loads(requests.get(url_access_token).text)['access_token']

        # get user id
        url_user_id = "https://graph.facebook.com/debug_token?" + user_token + access_token
        user_id = json.loads(requests.get(url_user_id).text)['data']['user_id']

        # get user info
        url_user_obj = 'https://graph.facebook.com/v2.9/' + \
            user_id + '?access_token=' + access_token
        user_obj = json.loads(requests.get(url_user_obj).text)

        # store user info
        set_user_id(request.session.session_key, user_id)
        user = FacebookUser.objects.get_or_create(user_id=user_id)[0]
        user.username = user_obj['name']
        user.save()

    return redirect(UNIVERSAL_URL.format(str(redirect_service)))


@never_cache
def user_logout(request):
    if not request.session.session_key:
        request.session.save()
    del_user_id(request.session.session_key)

    redirect_service = request.GET.get('redirect_service')
    return redirect(UNIVERSAL_URL(str(redirect_service)))


@never_cache
def user_get(request):
    if not request.session.session_key:
        request.session.save()

    user_id = get_user_id(request.session.session_key)
    if user_id != None:
        user = FacebookUser.objects.get(user_id=user_id.decode('utf-8'))
        if '' in (user.school, user.career, user.major):
            profile = None
        else:
            profile = {
                'school': user.school,
                'career': user.career,
                'major': user.major,
                'grade': user.grade
            }
        res = {'id': user.user_id, 'name': user.username,
               'verify': request.session.session_key, 'profile': profile}
        return JsonResponse(res)
    return HttpResponse(None)


@never_cache
def user_verify(request, v_id, v_key):
    user_id = get_user_id(v_key)
    if user_id != None:
        user = FacebookUser.objects.get(user_id=user_id.decode('utf-8'))
        if user.user_id == v_id:
            return HttpResponse('Ok')
    return HttpResponse(None)


@never_cache
def user_edit(request, user_id, school, career, major, grade):
    if not request.session.session_key:
        request.session.save()

    if user_id != None:
        user = FacebookUser.objects.get(user_id=user_id)
        user.school = school
        user.career = career
        user.major = major
        user.grade = int(grade)
        user.save()
        return HttpResponse('Ok')
    return HttpResponse(None)
