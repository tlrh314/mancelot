from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry

from catalogue.utils import CeceApiClient
from catalogue.utils import CommandWrapper
from catalogue.models import (
    PaymentOption,
    Store,
)


def create_or_update_stores(logger, cmd_name, client):
    fn = "create_or_update_stores"
    client.set_cece_token_headers(logger)

    uri = settings.CECE_API_URI + "mancelot/catalog/store/"
    logger.debug("{0}: GET {1}".format(fn, uri))
    data = client.get_list(logger, uri, recursive=True)
    logger.debug("{0}: received {1} stores".format(fn, len(data)))

    store_ctpk = ContentType.objects.get_for_model(Store).pk
    paymentoption_ctpk = ContentType.objects.get_for_model(PaymentOption).pk

    logger.debug("\n{0}: create/update".format(fn))
    for i, s in enumerate(data):
        logger.debug("{0} / {1}".format(i, len(data) ))
        store, created = Store.objects.get_or_create(
            name=s["store_name"],
            info=s["about"],
            url=s["store_url"],
            logo=s["logo"],
            cece_api_url="{0}{1}/".format(uri, s["id"]),
            last_updated_by=client.ceceuser,
        )
        # TODO: download logo, set url to mancelot.nl
        logger.debug("  {0} Store: {1}".format("Created" if created else "Have", store))
        if created:
            LogEntry.objects.log_action(
                client.ceceuser.pk, store_ctpk, store.pk, str(store), ADDITION,
                change_message="Created by '{0}'".format(cmd_name))
            store.save()

        # Related field: external pay_methods is M2M, serializes as string (name)
        for pm in s["pay_methods"]:
            paymentoption, created = PaymentOption.objects.get_or_create(name=pm)
            logger.debug("    {0} PaymentOption: {1}".format(
                "Created" if created else "Have", paymentoption))
            if created:
                paymentoption.last_updated_by = client.ceceuser
                LogEntry.objects.log_action(
                    client.ceceuser.pk, paymentoption_ctpk, paymentoption.pk, str(paymentoption), ADDITION,
                    change_message="Created by '{0}'".format(cmd_name))
                paymentoption.save()
            store.payment_options.add(paymentoption); store.save()


class Command(CommandWrapper):
    help = "Update our database with Store instances from the Cece API"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_stores
        self.margs = [self.cmd_name, client]
        self.mkwargs = {}

        super().handle(*args, **options)

