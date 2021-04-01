from django.conf import settings
from celery.utils.log import get_task_logger

from settings.celery import app
from accounts.models import (
    UserModel,
    # Order,
)

logger = get_task_logger(__name__)


@app.task
def talk_to_mollie_api():
    # mc = MollieClient()
    # mc.set_api_key(settings.MOLLIE_API_KEY_TEST if settings.DEBUG else settings.MOLLIE_API_KEY_LIVE)
    payment = mc.payments.create(
        {
            "amount": {"currency": "EUR", "value": "10.00"},
            "description": "My first API payment",
            "redirectUrl": "https://webshop.example.org/order/12345/",
            "webhookUrl": "https://webshop.example.org/mollie-webhook/",
        }
    )

    payment = mollie_client.payments.get(payment.id)

    if payment.is_paid():
        print("Payment received.")
