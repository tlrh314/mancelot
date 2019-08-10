from __future__ import absolute_import, unicode_literals
from settings.base import *

# NB, Load the filebrowser settings after base to ensure SECRET_KEY is set
from filebrowser.sites import site
from django.core.files.storage import FileSystemStorage
site.storage = FileSystemStorage(
    location=STATIC_ROOT,
    base_url=STATIC_URL
)
site.directory = "img/"


# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
__all__ = ("celery_app",)
