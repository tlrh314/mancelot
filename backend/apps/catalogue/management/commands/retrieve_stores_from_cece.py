from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry

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
        store.logo = s["logo"]
        # TODO: download logo, set url to mancelot.nl
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

            if created:
                # Log Created to PaymentOption instance only if created
                paymentoption.last_updated_by = client.ceceuser
                LogEntry.objects.log_action(
                    user_id=client.ceceuser.pk,
                    content_type_id=paymentoption_ctpk,
                    object_id=paymentoption.pk,
                    object_repr=str(paymentoption),
                    action_flag=ADDITION if created else CHANGE,
                    change_message="Created by '{0}'".format(cmd_name),
                )
                paymentoption.save()

            # Add the paymentoption to the brand, and log to Store instance
            store.payment_options.add(paymentoption)
            LogEntry.objects.log_action(
                user_id=client.ceceuser.pk,
                content_type_id=store_ctpk,
                object_id=store.pk,
                object_repr=str(store),
                action_flag=ADDITION if created else CHANGE,
                change_message="PaymentOption '{0}' added by '{1}'".format(
                    paymentoption.name, cmd_name
                )
            )
            store.save()


class Command(CommandWrapper):
    help = "\033[91mUpdate Stores with Cece data, overwriting all fields!\033[0m\n"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_stores
        self.margs = [ self.cmd_name, client ]
        self.mkwargs = { "recursive": True if settings.DEBUG else False }

        super().handle(*args, **options)

