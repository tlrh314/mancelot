import os
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry

from catalogue.utils import call_download_image
from catalogue.utils import CeceApiClient
from catalogue.utils import CommandWrapper
from catalogue.models import (
    PaymentOption,
    Store,
)


def create_or_update_stores(logger, cmd_name, client, recursive=True):
    fn = "create_or_update_stores"
    client.set_cece_token_headers(logger)

    # Retrieve the (paginated) data
    uri = settings.CECE_API_URI + "mancelot/catalog/store/"
    logger.debug("{0}: GET {1} <-- recursive = {2}".format(fn, uri, recursive))
    data = client.get_list(logger, uri, recursive=recursive)
    logger.debug("{0}: received {1} stores".format(fn, len(data)))

    # Get the ContentType pks for the LogEntry
    store_ctpk = ContentType.objects.get_for_model(Store).pk
    paymentoption_ctpk = ContentType.objects.get_for_model(PaymentOption).pk

    # Iterate through the Cece data
    for i, s in enumerate(data):
        logger.debug("\n{0} / {1}".format(i+1, len(data) ))

        # Get or create Store. Match on **name** only!
        store, created = Store.objects.get_or_create(
            name=s["store_name"],
        )
        logger.debug("{0} Store: {1}".format("Created" if created else "Have", store))

        # Overwrite all fields
        store.info = s["about"]
        store.url = s["store_url"]
        cece_logo_url = s["logo"]
        store.cece_api_url = "{0}{1}/".format(uri, s["id"])
        store.last_updated_by = client.ceceuser

        # Log Created/Updated to Store instance
        LogEntry.objects.log_action(
            user_id=client.ceceuser.pk,
            content_type_id=store_ctpk,
            object_id=store.pk,
            object_repr=str(store),
            action_flag=ADDITION if created else CHANGE,
            change_message="{0} by '{1}'".format(
                "Created" if created else "Updated", cmd_name
            )
        )
        store.save()

        # Related field: external pay_methods is M2M, serializes as string (name)
        for pm in s["pay_methods"]:
            # Get or created PaymentOption. Match on **name** only!
            paymentoption, created = PaymentOption.objects.get_or_create(name=pm)
            logger.debug("  {0} PaymentOption: {1}".format(
                "Created" if created else "Have", paymentoption))
            store.payment_options.add(paymentoption)
            store.save()

        ### Download the logo. Data format is (usually) a full url
        # TODO: if "http" not in cece_logo_url: add it?
        logger.debug("  Fetch '{0}' from Cece".format(cece_logo_url))
        fname = os.path.basename(urlparse(cece_logo_url).path)
        save_to = "{0}/img/logos/stores/{1}".format(settings.STATIC_ROOT, fname)
        call_download_image(logger, cece_logo_url, save_to,
            store, "logo", store_ctpk, client.ceceuser.pk, cmd_name
        )
        ### End of logo download


class Command(CommandWrapper):
    help = "\033[91mUpdate Stores with Cece data, overwriting all fields!\033[0m\n"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_stores
        self.margs = [ self.cmd_name, client ]
        self.mkwargs = { "recursive": not settings.DEBUG }

        super().handle(*args, **options)

