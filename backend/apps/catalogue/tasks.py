import os
import time

from django.conf import settings
from celery.utils.log import get_task_logger
from django.core.management import call_command
from django.utils.module_loading import import_string

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
    for script in [
            # inserts/updates the 'info' field (which retrieve_brands_from_cece does not!)
            "retrieve_labels_from_cece",
            "retrieve_certificates_from_cece",

            # also adds Subcategory instances to Category instances
            "retrieve_categories_from_cece",

            # inserts/updates the 'icon_url' field (which retrieve_stores_from_cece does not!)
            "retrieve_paymethods_from_cece",

            # also adds PaymentOptions ('name' only) to Store instances
            "retrieve_stores_from_cece",

            # also adds CeceLabels / Certificates ('name' only) to Brand instances
            "retrieve_brands_from_cece",

            # also adds Size/Color/Material ('name' only) to Product instances
            "retrieve_products_from_cece",
    ]:
        call_command( script, "--is_task" )

@app.task
def update_exchange_rates(backend=settings.EXCHANGE_BACKEND, **kwargs):
    backend = import_string(backend)()
    backend.update_rates(**kwargs)
