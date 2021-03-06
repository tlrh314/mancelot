import os
import sys

import environ
from django.utils.translation import ugettext_lazy as _

### We use django-environ to read secrets from .env file
env = environ.Env()
env.read_env(str((environ.Path(__file__) - 1).path(".env")))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Use the "apps" folder for our project apps
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# `env LC_CTYPE=C tr -dc "a-zA-Z0-9" < /dev/random | head -c 50; echo`
SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG", default=False)

DATABASES = {
    "default": env.db("DATABASE_URL"),
}

CACHES = {"default": env.cache()}

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    # FileBrowser must be loaded before Django admin
    "tinymce",
    "filebrowser",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_celery_beat",
    "django_celery_results",
    "django_countries",
    "django_filters",
    "corsheaders",
    "rest_framework",
    # "rest_framework_simplejwt.token_blacklist",
    "silk",
    "djmoney",
    "djmoney.contrib.exchange",
    "accounts",
    "catalogue",
]

SITE_ID = 1

MIDDLEWARE = [
    # "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "corsheaders.middleware.CorsPostCsrfMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "silk.middleware.SilkyMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = "settings.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],  # templates shared between apps
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "context_processors.set_meta_tags",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "settings.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Cookie settings
CSRF_COOKIE_HTTPONLY = (
    False  # to allow the front-end to retrieve CSRF token from the Cookie
)
CSRF_COOKIE_SAMESITE = "Strict"  # TODO: exactly what will the front-end be doing?
CSRF_COOKIE_SECURE = True

# Security headers --> already set by nginx
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", _("English")),
    ("nl", _("Nederlands")),
]

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = ((os.path.join(BASE_DIR, u"locale/")),)

CURRENCIES = ("EUR", "GBP", "USD")
CURRENCY_CHOICES = [("EUR", "EUR €"), ("GBP", "GBP £"), ("USD", "USD $")]
BASE_CURRENCY = "EUR"
DEFAULT_CURRENCY = "EUR"
CURRENCY_DECIMAL_PLACES = 4
OPEN_EXCHANGE_RATES_APP_ID = env("OPEN_EXCHANGE_RATES_APP_ID")
EXCHANGE_BACKEND = "djmoney.contrib.exchange.backends.OpenExchangeRatesBackend"
MOLLIE_API_KEY_LIVE = env("MOLLIE_API_KEY_LIVE")
MOLLIE_API_KEY_LIVE = env("MOLLIE_API_KEY_LIVE")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
PREPEND_WWW = True
APPEND_SLASH = True

AUTH_USER_MODEL = "accounts.UserModel"
LOGIN_URL = "admin:login"
LOGIN_REDIRECT_URL = "accounts:profile"
ADMIN_BCC = []

SERVER_EMAIL = "django@mancelot.app"
DEFAULT_FROM_EMAIL = "info@mancelot.app"
EMAIL_CONFIG = env.email_url("EMAIL_URL")
vars().update(EMAIL_CONFIG)

# List of who will receive code error notifications. Not used b/c Sentry
ADMINS = []  # use tuples, i.e. ("Full name", "email@example.com")
# List of who will receive broken link emails
MANAGERS = []


### Celery Task Scheduler
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_TIMEZONE = TIME_ZONE


### Django REST Framework for API endpoints
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.DjangoModelPermissions"],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "TEST_REQUEST_RENDERER_CLASSES": [
        "rest_framework.renderers.MultiPartRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer",
    ],
}
### Django REST Simple JWT
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": (
        "rest_framework_simplejwt.tokens.AccessToken",
    ),  # or SlidingToken
    "TOKEN_TYPE_CLAIM": "token_type",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=30),
}

# True --> CORS_ORIGIN_WHITELIST not used and all origins will be accepted
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    "https://mancelot.app",
    "https://www.mancelot.app",
    "http://localhost",
    "http://localhost:3000",
]
CSRF_TRUSTED_ORIGINS = [  # TODO
    "mancelot.app",
]
CORS_ALLOW_METHODS = [  # Default, but explicitly added to settings
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [  # Default, but explicitly added to settings
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Silky for profiling / monitoring the api response times
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True  # default is_staff=True; overwrite below
SILKY_PERMISSIONS = lambda user: user.is_superuser
SILKY_PYTHON_PROFILER = False
SILKY_PYTHON_PROFILER_BINARY = False
# SILKY_MAX_REQUEST_BODY_SIZE = -1     # Silk takes anything <0 as no limit
# SILKY_MAX_RESPONSE_BODY_SIZE = 1024  # If response body>1024 bytes, ignore
# SILKY_INTERCEPT_PERCENT = 50 # log only 50% of requests
# SILKY_MAX_RECORDED_REQUESTS = 10**4  # garbage collection of old data
# SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = 10
SILKY_META = True  # to check the effect Silk itself has on response time


### Sentry for error reporting
SENTRY_DSN_API = env("SENTRY_DSN_API", default="")
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=SENTRY_DSN_API,
    integrations=[DjangoIntegration()],
    environment=env("SENTRY_ENVIRONMENT"),
)

CECE_API_USER = env("CECE_API_USER", default="secret")
CECE_API_PASS = env("CECE_API_PASS", default="secret")
CECE_API_URI = env("CECE_API_URI", default="http://example.com")

MANCELOT_KVK_NUMMER = env("MANCELOT_KVK_NUMMER")
MANCELOT_BTW_NUMMER = env("MANCELOT_BTW_NUMMER")


### FileBrowser to tinker with static files at the server
# http://django-filebrowser.readthedocs.io/en/latest/settings.html
# DIRECTORY = ""
FILEBROWSER_DIRECTORY = ""
FILEBROWSER_DEFAULT_PERMISSIONS = 0o644
FILEBROWSER_OVERWRITE_EXISTING = True
FILEBROWSER_EXTENSIONS = {
    "Image": [".jpg", ".jpeg", ".gif", ".png", ".tif", ".tiff"],
    "Document": [".pdf", ".doc", ".rtf", ".txt", ".xls", ".csv"],
    "Video": [".mov", ".wmv", ".mpeg", ".mpg", ".avi", ".rm"],
    "Audio": [".mp3", ".mp4", ".wav", ".aiff", ".midi", ".m4p"],
}
FILEBROWSER_ADMIN_VERSIONS = ["big", "thumbnail", "small", "medium", "large"]


### TinyMCE as WYSIWYG editor in the FileBrowser
# https://www.tinymce.com/docs/demo/full-featured/
TINYMCE_DEFAULT_CONFIG = {
    "selector": "textarea",
    "height": 500,
    "theme": "modern",
    "plugins": [
        "advlist autolink lists link image charmap print preview hr anchor pagebreak",
        "searchreplace wordcount visualblocks visualchars code fullscreen",
        "insertdatetime media nonbreaking save table contextmenu directionality",
        "emoticons template paste textcolor colorpicker textpattern imagetools codesample toc",
    ],
    "toolbar1": "undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image",
    "toolbar2": "print preview image | forecolor backcolor emoticons | codesample",
    "image_advtab": True,
    "templates": [
        {"title": "Test template 1", "content": "Test 1"},
        {"title": "Test template 2", "content": "Test 2"},
    ],
    "content_css": [
        "//www.tinymce.com/css/codepen.min.css",
        # "/static/css/main.css",
    ],
}
# TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True
TINYMCE_FILEBROWSER = True
TINYMCE_MINIMAL_CONFIG = {
    "selector": "textarea",
    "height": 80,
    "width": 500,
    "menubar": False,
    "statusbar": False,
    "elementpath": False,
    "plugins": [
        "link paste autolink code",
    ],
    "toolbar1": "undo redo | bold italic | bullist numlist outdent indent | link code",
    "toolbar2": "",
}


import logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "console": {
            "format": "{message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "log/request.log",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": True,
        },
        "file": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "console": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

if DEBUG or True:
    PREPEND_WWW = False

    INSTALLED_APPS += [
        "django_extensions",
    ]

    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += [
        "rest_framework.renderers.BrowsableAPIRenderer",
    ]
