# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import os

import django

ROOT_DIR = os.path.dirname(__file__)

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "countries_plus",
]

SITE_ID = 1

ROOT_URLCONF = 'tests.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(ROOT_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'countries_plus.context_processors.add_request_country',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    },
]
if django.VERSION >= (1, 10):
    MIDDLEWARE = ('countries_plus.middleware.AddRequestCountryMiddleware',)
else:
    MIDDLEWARE_CLASSES = ('countries_plus.middleware.AddRequestCountryMiddleware',)

COUNTRIES_PLUS_COUNTRY_HEADER = 'GEOIP_HEADER'
COUNTRIES_PLUS_DEFAULT_ISO = 'US'
