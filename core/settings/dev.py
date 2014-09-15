from .includes.common import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "dsnac",
        "USER": "dsnac",
        "PASSWORD": DBPASSWORD,
        "HOST": "",
        "PORT": ""}}

VIRTUALENV = 'dsnac'

SITE_TITLE = 'Sikh National Archives of Canada'
SITE_TAGLINE = None
