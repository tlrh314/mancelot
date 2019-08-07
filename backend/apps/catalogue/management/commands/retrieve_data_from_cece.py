import os
import sys
import logging

from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry

from accounts.models import UserModel
from catalogue.utils import format_time_diff
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


ADMIN = UserModel.objects.first()
CMD_NAME = __file__.split("/")[-1].replace(".py", "")


def update_cecelabel_instances():
    return
    label = CeceLabel.objects.none()
    # Check which instanes have not been updated for X time

    # GET the Cece endpoint to retrieve the data, then update our database

    # Update the LogEntry
    content_type_pk = ContentType.objects.get_for_model(CeceLabel).pk
    LogEntry.objects.log_action(
        ADMIN.pk, content_type_pk, label.pk, str(label), CHANGE,
        change_message="{0}".format(CMD_NAME))
    label.save()


def update_certificate_instances():
    return
    certificate = Certificate.objects.none()
    # Check which instanes have not been updated for X time

    # GET the Cece endpoint to retrieve the data, then update our database

    # Update the LogEntry
    content_type_pk = ContentType.objects.get_for_model(Certificate).pk
    LogEntry.objects.log_action(
        ADMIN.pk, content_type_pk, certificate.pk, str(certificate), CHANGE,
        change_message="{0}".format(CMD_NAME))
    certificate.save()


def update_category_instances():
    return
    category = Category.objects.none()
    # Check which instanes have not been updated for X time

    # GET the Cece endpoint to retrieve the data, then update our database

    # Update the LogEntry
    content_type_pk = ContentType.objects.get_for_model(Category).pk
    LogEntry.objects.log_action(
        ADMIN.pk, content_type_pk, category.pk, str(category), CHANGE,
        change_message="{0}".format(CMD_NAME))
    category.save()


def update_subcategory_instances():
    return
    subcategory = Subcategory.objects.none()
    # Check which instanes have not been updated for X time

    # GET the Cece endpoint to retrieve the data, then update our database

    # Update the LogEntry
    content_type_pk = ContentType.objects.get_for_model(Subcategory).pk
    LogEntry.objects.log_action(
        ADMIN.pk, content_type_pk, subcategory.pk, str(subcategory), CHANGE,
        change_message="{0}".format(CMD_NAME))
    subcategory.save()


def update_paymentoption_instances():
    return
    payment_option = PaymentOption.objects.none()
    # Check which instanes have not been updated for X time

    # GET the Cece endpoint to retrieve the data, then update our database

    # Update the LogEntry
    content_type_pk = ContentType.objects.get_for_model(PaymentOption).pk
    LogEntry.objects.log_action(
        ADMIN.pk, content_type_pk, payment_option.pk, str(payment_option), CHANGE,
        change_message="{0}".format(CMD_NAME))
    payment_option.save()


def update_store_instances():
    return
    store = Store.objects.none()
    # Check which instanes have not been updated for X time

    # GET the Cece endpoint to retrieve the data, then update our database

    # Update the LogEntry
    content_type_pk = ContentType.objects.get_for_model(Store).pk
    LogEntry.objects.log_action(
        ADMIN.pk, content_type_pk, store.pk, str(store), CHANGE,
        change_message="{0}".format(CMD_NAME))
    store.save()


def update_brand_instances():
    return
    brand = Brand.objects.none()
    # Check which instanes have not been updated for X time

    # GET the Cece endpoint to retrieve the data, then update our database

    # Update the LogEntry
    content_type_pk = ContentType.objects.get_for_model(Brand).pk
    LogEntry.objects.log_action(
        ADMIN.pk, content_type_pk, brand.pk, str(brand), CHANGE,
        change_message="{0}".format(CMD_NAME))
    brand.save()


def update_product_instances():  # will update Size and Material instances
    return
    product = Product.objects.none()
    # Check which instanes have not been updated for X time

    # GET the Cece endpoint to retrieve the data, then update our database

    # Update the LogEntry
    content_type_pk = ContentType.objects.get_for_model(Product).pk
    LogEntry.objects.log_action(
        ADMIN.pk, content_type_pk, product.pk, str(product), CHANGE,
        change_message="{0}".format(CMD_NAME))
    product.save()


class Command(BaseCommand):
    help = "Update our database with data from the Cece API"

    def add_arguments(self, parser):
        parser.add_argument("--is_task",
            dest="is_task", action="store_true", default=False,
            help="The task outputs to console and logfile. When using --is_task, "+\
            "the console output is silenced, thus, we only log to file."
        )

    def handle(self, *args, **options):
        is_task = options["is_task"]

        logdir = "/mancelot/log/commands"
        if not os.path.exists(logdir): os.makedirs(logdir)
        logfilename = "{0}/{1}.txt".format(logdir, CMD_NAME)
        with open(logfilename, "w"):
            # clean up any existing logfile by opening it and writing empty file
            pass

        logger = logging.getLogger("console")
        if is_task: logger.handlers = []  # do not log to console
        logger.addHandler(logging.FileHandler(filename=logfilename))  # always log to file

        start_time = timezone.localtime(timezone.now())
        logger.info("manage {0}: begonnen, is_task={1}".format(CMD_NAME, is_task))
        logger.info("Begintijd: {0}\n".format(timezone.localtime(
            start_time).strftime("%d/%m/%YT%H:%M:%S")))

        update_cecelabel_instances()
        update_certificate_instances()
        update_category_instances()
        update_subcategory_instances()
        update_paymentoption_instances()
        update_store_instances()
        update_brand_instances()
        update_product_instances()  # will update Size and Material instances

        end_time = timezone.now()
        logger.info("\n----------")
        logger.info("Eindtijd: {0}".format(timezone.localtime(
            end_time).strftime("%d/%m/%YT%H:%M:%S")))
        logger.info("Runtijd: {0}".format(format_time_diff(start_time, end_time)))
        logger.info("manage.py {0}: geeindigd.".format(CMD_NAME))

