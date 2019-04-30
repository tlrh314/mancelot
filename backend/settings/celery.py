import os
import sys
from celery import Celery

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Use the 'apps' folder for our project apps
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('settings')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
