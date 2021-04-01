from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from catalogue.utils import CeceApiClient
from catalogue.utils import CommandWrapper
from catalogue.models import (
    Category,
    Subcategory,
)


def create_or_update_categories(logger, cmd_name, client, recursive=True):
    fn = "create_or_update_categories"
    client.set_cece_token_headers(logger)

    # Retrieve the (paginated) data
    uri = settings.CECE_API_URI + "mancelot/catalog/category/"
    logger.debug("{0}: GET {1}".format(fn, uri))
    data = client.get_list(logger, uri, recursive=recursive)
    logger.debug("{0}: received {1} brands".format(fn, len(data)))

    # Iterate through the Cece data
    section_map = {v: k for k, v in dict(Category.SECTIONS).items()}
    for i, c in enumerate(data):
        logger.debug("\n{0} / {1}".format(i + 1, len(data)))

        # Get or create Category. Match on **name** only!
        category, created = Category.objects.get_or_create(
            name=c["category_name"],
        )
        logger.debug(
            "{0} Category: {1}".format("Created" if created else "Have", category)
        )

        # Overwrite all fields
        try:
            section = section_map[c["type"]]
        except KeyError as e:
            logger.error(
                "\n\nERROR: encountered unknown section in Cece Category"
                + " '{0}'. Don't know what to do now.".format(c["type"])
            )
            raise
        cece_api_url = "{0}{1}/".format(uri, c["id"])
        category.save()

        # Related field: external subcategory is M2M, serializes as string (name)
        for l in c["subcategory"]:
            subcategory, created = Subcategory.objects.get_or_create(
                name=l["sub_name"],
                category=category,
            )
            logger.debug(
                "  {0} Subcategory : {1}".format(
                    "Created" if created else "Have", subcategory
                )
            )
            subcategory.save()


class Command(CommandWrapper):
    help = "Update our database with Brand instances from the Cece API"
    help = "\033[91mUpdate [Sub]Categories with Cece data, overwriting all fields!\033[0m\n"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_categories
        self.margs = [self.cmd_name, client]
        self.mkwargs = {"recursive": not settings.DEBUG}

        super().handle(*args, **options)
