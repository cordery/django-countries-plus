import django

APP_NAME = 'countries_plus'
__version__ = '2.1.0'

if django.VERSION[0] == 2:
    default_app_config = 'countries_plus.apps.DefaultConfig'
