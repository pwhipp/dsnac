from .includes.common import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }}

VIRTUALENV = 'dsnac'

SITE_TITLE = 'Sikh National Archives of Canada'
SITE_TAGLINE = None
