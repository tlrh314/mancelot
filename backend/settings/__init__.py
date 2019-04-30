from settings.base import *


# NB, Load the filebrowser settings after base to ensure SECRET_KEY is set
from filebrowser.sites import site
from django.core.files.storage import FileSystemStorage
site.storage = FileSystemStorage(location="/mancelot/static", base_url="/static/")
site.directory = "img/"
