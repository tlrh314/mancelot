import os
import sys
import environ

### We use django-environ to read secrets from .env file
env = environ.Env()
env.read_env(
    str((environ.Path(__file__) - 1).path(".env"))
)

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

CACHES = {
    "default": env.cache()
}

ALLOWED_HOSTS = [
    "localhost",
    env("ALLOWED_HOST1"),
    env("ALLOWED_HOST2")
]


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
    "django_extensions",
    "django_filters",
    "rest_framework",
    "rest_framework_datatables",

    "accounts",
    "catalogue",
]

SITE_ID = 1

MIDDLEWARE = [
    # "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "nl-nl"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

AUTH_USER_MODEL = "accounts.UserModel"
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:profile"
ADMIN_BCC = []

SERVER_EMAIL = "django@mancelot.nl"
DEFAULT_FROM_EMAIL = "info@mancelot.nl"
EMAIL_CONFIG = env.email_url("EMAIL_URL")
vars().update(EMAIL_CONFIG)


### Celery Task Scheduler
CELERY_BROKER_URL = env.cache("CELERY_REDIS")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND = "django-db"
# CELERY_RESULT_BACKEND = env.cache("CELERY_REDIS")
CELERY_CACHE_BACKEND = "django-cache"


### Django REST Framework for API endpoints
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework_datatables.renderers.DatatablesRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework_datatables.filters.DatatablesFilterBackend",
        ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework_datatables.pagination.DatatablesPageNumberPagination",
    "PAGE_SIZE": 50
}
### Django REST Simple JWT
from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}



### Sentry for error reporting
SENTRY_DSN_API = env("SENTRY_DSN_API", default="")
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
sentry_sdk.init(
    dsn=SENTRY_DSN_API,
    integrations=[DjangoIntegration()],
    environment=env("SENTRY_ENVIRONMENT")
)


### FileBrowser to tinker with static files at the server
# http://django-filebrowser.readthedocs.io/en/latest/settings.html
# DIRECTORY = ""
FILEBROWSER_DIRECTORY = ""
FILEBROWSER_DEFAULT_PERMISSIONS = 0o644
FILEBROWSER_EXTENSIONS = {
    "Image": [".jpg", ".jpeg",".gif",".png",".tif",".tiff"],
    "Document": [".pdf", ".doc",".rtf",".txt",".xls",".csv"],
    "Video": [".mov",".wmv",".mpeg",".mpg",".avi",".rm"],
    "Audio": [".mp3",".mp4",".wav",".aiff",".midi",".m4p"]
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
    "emoticons template paste textcolor colorpicker textpattern imagetools codesample toc"
  ],
  "toolbar1": "undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image",
  "toolbar2": "print preview image | forecolor backcolor emoticons | codesample",
  "image_advtab": True,
  "templates": [
    { "title": "Test template 1", "content": "Test 1" },
    { "title": "Test template 2", "content": "Test 2" }
  ],
  "content_css": [
    "//fonts.googleapis.com/css?family=Lato:300,300i,400,400i",
    "//www.tinymce.com/css/codepen.min.css",
    "/static/css/main.css",
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
    "toolbar2": ""
}