"""
Django settings for userpool project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Domain name
DOMAIN = 'campass.com.tw'
UNIVERSAL_URL = 'https://{}.campass.com.tw'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open(BASE_DIR + '/config/' + 'secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# DEBUG = True

ALLOWED_HOSTS = ['.' + DOMAIN, 'localhost', '127.0.0.1', '0.0.0.0']


# Application definition

REQUIRED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
]

PROJECT_APPS = [
    'login.apps.LoginConfig',
]

INSTALLED_APPS = REQUIRED_APPS + PROJECT_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'userpool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'userpool.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_PROFILE_MODULE = 'login.UserProfile'


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Settings for our specific uses

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

from .settings_database import DATABASE_SETTINGS
if DEBUG:
    DATABASES = DATABASE_SETTINGS['sqlite']
else:
    DATABASES = DATABASE_SETTINGS['mysql']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Shared session

SESSION_COOKIE_DOMAIN = '.' + DOMAIN
with open(BASE_DIR + '/config/' + 'sessionid.txt') as f:
    SESSION_COOKIE_NAME = f.read().strip()

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Cache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# HTTPS

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# CORS header

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_REGEX_WHITELIST = (
    '^(https?://)www.' + DOMAIN,
    '^(https?://)localhost$',
    '(https?://)127.0.0.1'
)
CORS_ALLOW_METHODS = (
    'GET',
)

# Facebook App

with open(BASE_DIR + '/config/' + 'fb_app_id.txt') as f:
    FB_APP_ID = f.read().strip()

with open(BASE_DIR + '/config/' + 'fb_app_sec.txt') as f:
    FB_APP_SEC = f.read().strip()

# Dev

if DEBUG:
    del SESSION_COOKIE_DOMAIN
    del SECURE_PROXY_SSL_HEADER
    SECURE_SSL_REDIRECT = False
    CORS_ORIGIN_ALLOW_ALL = True
    UNIVERSAL_URL = 'http://test.localhost.{}.campass.com.tw:8080'
