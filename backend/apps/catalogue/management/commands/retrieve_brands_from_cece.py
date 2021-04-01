from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from catalogue.utils import CeceApiClient
from catalogue.utils import CommandWrapper
from catalogue.models import (
    CeceLabel,
    Certificate,
    Brand,
)


def create_or_update_brands(logger, cmd_name, client, recursive=True):
    fn = "create_or_update_brands"
    client.set_cece_token_headers(logger)

    # Retrieve the (paginated) data
    uri = settings.CECE_API_URI + "mancelot/catalog/brand/"
    logger.debug("{0}: GET {1} <-- recursive = {2}".format(fn, uri, recursive))
    data = client.get_list(logger, uri, recursive=recursive)
    logger.debug("{0}: received {1} brands".format(fn, len(data)))

    # Iterate through the Cece data
    for i, b in enumerate(data):
        logger.debug("\n{0} / {1}".format(i + 1, len(data)))

        # Get or create Brand. Match on **name** only!
        brand, created = Brand.objects.get_or_create(
            name=b["brand_name"],
        )
        logger.debug(
            "{0} Brand: {1}".format("Created" if created else "Updated", brand)
        )

        # Overwrite all fields
        brand.info = b["about_brand"]
        brand.cece_api_url = "{0}{1}/".format(uri, b["id"])
        brand.last_updated_by = client.ceceuser
        brand.save()

        # Related field: external labels is M2M, serializes as string (name)
        for l in b["labels"]:
            # Get or create CeceLabel. Match on **name** only!
            label, created = CeceLabel.objects.get_or_create(name=l["label_name"])
            logger.debug(
                "  {0} CeceLabel: {1}".format("Created" if created else "Have", label)
            )
            brand.labels.add(label)
            brand.save()

        # Related field: external labels is M2M, serializes as string (name)
        for c in b["certificate"]:
            # Get or create Certificate. Match on **name** only!
            certificate, created = Certificate.objects.get_or_create(name=c)
            logger.debug(
                "  {0} Certificate: {1}".format(
                    "Created" if created else "Have", certificate
                )
            )
            brand.certificates.add(certificate)
            brand.save()


class Command(CommandWrapper):
    help = "\033[91mUpdate Brands with Cece data, overwriting all fields!\033[0m\n"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_brands
        self.margs = [self.cmd_name, client]
        self.mkwargs = {"recursive": not settings.DEBUG}

        super().handle(*args, **options)
