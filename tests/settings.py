import os

import django  # noqa: F401

from .generated_settings import *  # noqa: F403

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "countries_plus",
]

TEMPLATES[0]["DIRS"] = [os.path.join(BASE_DIR, "templates")]  # noqa: F405
