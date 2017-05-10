from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from django.views.decorators.cache import never_cache

import requests, json
from login.models import FacebookUser

import userpool.settings

def login(request):
    redirect_service = request.GET.get('redirect_service')
    client_id = "client_id=199021993947051"
    client_sec = "&client_secret=9d7f81f67f0df142040160fb975192a7"
    redirect_uri = "&redirect_uri=" + "http://test.localhost.login.campass.com.tw:8080/fb?redirect_service=" + redirect_service
    code = "&code=" + str(request.GET.get('code'))

    url_user_token = "https://graph.facebook.com/v2.9/oauth/access_token?" + client_id + client_sec + redirect_uri + code
    user_token = "input_token=" + json.loads(requests.get(url_user_token).text)['access_token']

    url_app_token = "https://graph.facebook.com/v2.9/oauth/access_token?" + client_id + client_sec + "&grant_type=client_credentials"
    app_token = "&access_token=" + json.loads(requests.get(url_app_token).text)['access_token']

    url_user_id = "https://graph.facebook.com/debug_token?" + user_token + app_token
    user_id = json.loads(requests.get(url_user_id).text)['data']['user_id']

    import redis
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    redis_get = redis_client.get(request.session.session_key)
    if redis_get == None:
        # Register or Login
        redis_client.set(request.session.session_key, user_id)
        user = FacebookUser.objects.get_or_create(user_id=user_id)

    return redirect("http://" + 'test.localhost.' + str(redirect_service) + ".campass.com.tw:8080")

def logout(request):
    import redis
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    redis_client.delete(request.session.session_key)
    return HttpResponse('logged out')

@never_cache
def user(request):
    import redis
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    redis_get = redis_client.get(request.session.session_key)
    if redis_get == None:
        return HttpResponse(None)
    else:
        user = FacebookUser.objects.get(user_id=redis_get)
        res = {'user_id': user.user_id}
        return JsonResponse(res)
