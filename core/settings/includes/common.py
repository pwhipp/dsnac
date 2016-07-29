from __future__ import absolute_import, unicode_literals
from django.core.exceptions import ImproperlyConfigured

try:
    from .secrets import *
except ImportError:
    raise ImproperlyConfigured('You need a secrets.py file - contact paul.whipp@gmail.com')


PAGE_MENU_TEMPLATES = (
    (1, "Top navigation bar", "pages/menus/dropdown.html"),
    (2, "Footer", "pages/menus/footer.html"))


ADMINS = (
    ('Alexey Dubnyak', 'adubnyak@gmail.com'),
)
MANAGERS = ADMINS

ALLOWED_HOSTS = ['sikhnationalarchives.com']

TIME_ZONE = 'America/Montreal'

USE_I18N = False
USE_TZ = True
LANGUAGE_CODE = "en"
LANGUAGES = (
    ('en', 'English'),)

DEBUG = True

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

INTERNAL_IPS = ("127.0.0.1",)

TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader")

AUTHENTICATION_BACKENDS = (
    "mezzanine.core.auth_backends.MezzanineBackend",
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.browserid.BrowserIDBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.contrib.disqus.DisqusBackend',
    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    'social_auth.backends.contrib.orkut.OrkutBackend',
    'social_auth.backends.contrib.foursquare.FoursquareBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.live.LiveBackend',
    'social_auth.backends.contrib.skyrock.SkyrockBackend',
    'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
    'social_auth.backends.contrib.readability.ReadabilityBackend',
    'social_auth.backends.OpenIDBackend',
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder")

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644

import os

_dirs = os.path.abspath(__file__).split('/')
PROJECT_ROOT = BASE_DIR = '/'.join(_dirs[0:-4])  # Django 1.6 compat - PROJECT_ROOT is wrong name

CACHE_MIDDLEWARE_KEY_PREFIX = 'proposal_ea1ohDog'

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

FILEBROWSER_DIRECTORY = ''
BOOKS_ROOT = os.path.join(MEDIA_ROOT, 'books')
BOOKS_URL = MEDIA_URL + 'books/'
BOOKS_NO_COVER_IMAGE = os.path.join(MEDIA_URL, 'no_cover_image.png')

ROOT_URLCONF = 'core.urls'

TEMPLATE_DIRS = ()

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    'haystack',
    'theme',
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.pages",
    "mezzanine.galleries",
    "mezzanine.accounts",
    'social_auth',
    'djcelery',
    'paypal.standard.ipn',  # https://django-paypal.readthedocs.org/en/stable/
    'django_forms_bootstrap',
    "payments",  # https://stripe.com/docs/tutorials/charges
    'colorfield',

    'apps.bookrepo',
    'apps.bookreader',
    'apps.uploader',
    'apps.mediabooks',
    'apps.donate',
    'apps.userprofile',
    'apps.colours',
]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "mezzanine.conf.context_processors.settings",
    "mezzanine.pages.context_processors.page",
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
    'apps.colours.context_processors.colour_theme_processor'
)

MIDDLEWARE_CLASSES = (
    "mezzanine.core.middleware.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.RedirectFallbackMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
)

PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

SEARCH_MODEL_CHOICES = (
    'bookrepo.Book',
    'pages.Page',
    'blog.BlogPost')

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'layzfromlp@gmail.com'
EMAIL_HOST_PASSWORD = GMAIL_PASSWORD
EMAIL_PORT = 587
DEFAULT_EMAIL_FROM = 'support@sikhnationalarchives.org'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index')
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.",
        "NAME": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

TWITTER_CONSUMER_KEY = 'rj3AxmjrcWT06n0sbCj5GdSr4'
TWITTER_CONSUMER_SECRET = 'lwFInmiSRHcOtqOYRxkvEDCJuEsFfHK7qMY332zWM12IOeAW6B'
FACEBOOK_APP_ID = '343039815906340'
FACEBOOK_API_SECRET = 'cc4e0a2fdd6f8bf379f1d53820bbf1bb'
GOOGLE_OAUTH2_CLIENT_ID = '947939126600-e51bfah35mnuodbb7obsjfgt2a3pflh1.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'WOaPOc_R6jpMBMIJc67WY6ef'

SESSION_SERIALIZER ='django.contrib.sessions.serializers.PickleSerializer'

# LOGIN_URL          = '/login-form/'
LOGIN_REDIRECT_URL = '/'
# LOGIN_ERROR_URL    = '/login-error/'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/'
SOCIAL_AUTH_BACKEND_ERROR_URL = '/'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

import djcelery
djcelery.setup_loader()

CELERY_IMPORTS = ('bookrepo.tasks')

# PAYPAL_IDENTITY_TOKEN = 'AFcWxV21C7fd0v3bYYYRCpSSRl31AMrrMzliq4Yg5vTJIk2Ru-TIjf-f'
# PAYPAL_RECEIVER_EMAIL = 'adubnyak-facilitator@gmail.com'

PAYPAL_RECEIVER_EMAIL = 'sandeepsahota@gmail.com'  # '#Tf6*]w`!(juv}]
PAYPAL_IDENTITY_TOKEN = 'AVGIUS9goQDjVsvbAnWV3nRbap53tTjfHEBABDJfpKq7_28vDyqLaDusimbjDpt3b0Eufl-wHlej05sr'
PAYPAL_CLIENT_SECRET = 'ENcHz13UU5ml-jNEKm6cb4cF0h7rJas80MRAPUhYrjgu3BQ7p2ncCTFA_UO_Is-_QW6YYXCxSUyrTdVN'
PAYPAL_ACCESS_TOKEN = 'access_token$sandbox$tdyqc9w53w22yj38$1e5abc59f1832e2c2b2f5b30a1c4b4b9'

STRIPE_PUBLIC_KEY = 'pk_live_pvAiVzt4gkXmbxj69eknGHKv'
STRIPE_SECRET_KEY = 'sk_live_Vs9pcTv9P7JTfdDPQyKOsGxN'

AUTH_USER_MODEL = 'auth.User'
OPTIONAL_APPS = (
    "debug_toolbar",
    "django_extensions",
    "compressor",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())

try:
    from local_settings import *
except ImportError:
    pass
