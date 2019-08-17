from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry

from catalogue.utils import CeceApiClient
from catalogue.utils import CommandWrapper
from catalogue.models import (
    PaymentOption,
)


def create_or_update_paymentoptions(logger, cmd_name, client, recursive=True):
    fn = "create_or_update_paymentoptions"
    client.set_cece_token_headers(logger)

    # Retrieve the (paginated) data
    uri = settings.CECE_API_URI + "mancelot/catalog/paymethod/"
    logger.debug("{0}: GET {1} <-- recursive = {2}".format(fn, uri, recursive))
    data = client.get_list(logger, uri, recursive=recursive)
    logger.debug("{0}: received {1} paymethods".format(fn, len(data)))

    # Get the ContentType pks for the LogEntry
    paymentoption_ctpk = ContentType.objects.get_for_model(PaymentOption).pk

    # Iterate through the Cece data
    for i, pm in enumerate(data):
        logger.debug("\n{0} / {1}".format(i+1, len(data) ))

        # Get or create PaymentOption. Match on **name** only!
        paymentoption, created = PaymentOption.objects.get_or_create(
            name=pm["name"],
        )
        logger.debug("{0} PaymentOption: {1}".format("Created" if created else "Have", paymentoption))

        # Overwrite all fields
        paymentoption.info = pm["icon_url"]
        paymentoption.cece_api_url = "{0}{1}/".format(uri, pm["id"])
        paymentoption.last_updated_by = client.ceceuser

        # Log Created/Updated to PaymentOption instance
        LogEntry.objects.log_action(
            user_id=client.ceceuser.pk,
            content_type_id=paymentoption_ctpk,
            object_id=paymentoption.pk,
            object_repr=str(paymentoption),
            action_flag=ADDITION if created else CHANGE,
            change_message="{0} by '{1}'".format(
                "Created" if created else "Updated", cmd_name
            )
        )
        paymentoption.save()


class Command(CommandWrapper):
    help = "\033[91mUpdate PaymentOption with Cece data, overwriting all fields!\033[0m\n"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_paymentoptions
        self.margs = [ self.cmd_name, client ]
        self.mkwargs = { "recursive": True if settings.DEBUG else False }

        super().handle(*args, **options)
