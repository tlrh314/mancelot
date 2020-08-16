from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from catalogue.utils import CeceApiClient
from catalogue.utils import CommandWrapper
from catalogue.models import (
    Certificate,
)


def create_or_update_certificates(logger, cmd_name, client, recursive=True):
    fn = "create_or_update_certificates"
    client.set_cece_token_headers(logger)

    # Retrieve the (paginated) data
    uri = settings.CECE_API_URI + "mancelot/catalog/certificate/"
    logger.debug("{0}: GET {1} <-- recursive = {2}".format(fn, uri, recursive))
    data = client.get_list(logger, uri, recursive=recursive)
    logger.debug("{0}: received {1} certificates".format(fn, len(data)))

    # Iterate through the Cece data
    for i, c in enumerate(data):
        logger.debug("\n{0} / {1}".format(i+1, len(data) ))

        # Get or create Certificate. Match on **name** only!
        certificate, created = Certificate.objects.get_or_create(
            name=c["name"],
        )
        logger.debug("{0} Certificate: {1}".format("Created" if created else "Have", certificate))

        # Overwrite all fields
        certificate.info = c["about"]
        certificate.cece_api_url = "{0}{1}/".format(uri, c["id"])
        certificate.save()


class Command(CommandWrapper):
    help = "\033[91mUpdate Certificates with Cece data, overwriting all fields!\033[0m\n"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_certificates
        self.margs = [ self.cmd_name, client ]
        self.mkwargs = { "recursive": not settings.DEBUG }

        super().handle(*args, **options)
