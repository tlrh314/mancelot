import os
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from catalogue.utils import call_download_image
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

    # Iterate through the Cece data
    for i, pm in enumerate(data):
        logger.debug("\n{0} / {1}".format(i+1, len(data) ))

        # Get or create PaymentOption. Match on **name** only!
        paymentoption, created = PaymentOption.objects.get_or_create(
            name=pm["name"],
        )
        logger.debug("{0} PaymentOption: {1}".format("Created" if created else "Have", paymentoption))

        # Overwrite all fields
        cece_logo_url = pm["icon_url"]
        paymentoption.cece_api_url = "{0}{1}/".format(uri, pm["id"])
        paymentoption.save()

        ### Download the logo.
        fname = urlparse(cece_logo_url).path
        cece_logo_url = "https://www.projectcece.nl/static/{0}".format(fname)
        logger.debug("  Fetch '{0}' from Cece".format(cece_logo_url))

        save_to = "{0}/img/logos/payment/{1}".format(settings.STATIC_ROOT, os.path.basename(fname))

        call_download_image(logger, cece_logo_url, save_to,
            paymentoption, "logo", paymentoption_ctpk, client.ceceuser.pk, cmd_name
        )
        ### End of logo download


class Command(CommandWrapper):
    help = "\033[91mUpdate PaymentOption with Cece data, overwriting all fields!\033[0m\n"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_paymentoptions
        self.margs = [ self.cmd_name, client ]
        self.mkwargs = { "recursive": not settings.DEBUG }

        super().handle(*args, **options)
