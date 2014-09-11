from .includes.common import *

DEBUG = True

# Cache templates in production
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "dsnac",
        "USER": "dsnac",
        "PASSWORD": DBPASSWORD,
        "HOST": "",
        "PORT": ""}}

SITE_TITLE = 'The Proposal Generator'
SITE_TAGLINE = ''

###################
# DEPLOY SETTINGS #
###################

GUNICORN_BIND = "127.0.0.1:8000"
PROCESS_USER = 'dsnac'
PROCESS_NAME = 'dsnac_production'
VIRTUALENV = 'production'
