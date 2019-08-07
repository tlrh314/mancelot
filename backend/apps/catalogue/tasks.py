import os
import time

from django.conf import settings
from django.utils import timezone
from celery.utils.log import get_task_logger
from django.core.management import call_command

from settings.celery import app
from catalogue.models import (
    CeceLabel,
    Certificate,
    Category,
    Subcategory,
    PaymentOption,
    Store,
    Brand,
    Size,
    Material,
    Product
)

logger = get_task_logger(__name__)


@app.task
def retrieve_data_from_cece():
    call_command(
        "retrieve_data_from_cece",
        "--running_as_task"
    )
