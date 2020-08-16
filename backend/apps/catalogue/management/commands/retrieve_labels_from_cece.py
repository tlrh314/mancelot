from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from catalogue.utils import CeceApiClient
from catalogue.utils import CommandWrapper
from catalogue.models import (
    CeceLabel,
)


def create_or_update_labels(logger, cmd_name, client, recursive=True):
    fn = "create_or_update_labels"
    client.set_cece_token_headers(logger)

    # Retrieve the (paginated) data
    uri = settings.CECE_API_URI + "mancelot/catalog/label/"
    logger.debug("{0}: GET {1} <-- recursive = {2}".format(fn, uri, recursive))
    data = client.get_list(logger, uri, recursive=recursive)
    logger.debug("{0}: received {1} labels".format(fn, len(data)))

    # Iterate through the Cece data
    for i, l in enumerate(data):
        logger.debug("\n{0} / {1}".format(i+1, len(data) ))

        # Get or create CeceLabel. Match on **name** only!
        label, created = CeceLabel.objects.get_or_create(
            name=l["label_name"],
        )
        logger.debug("{0} CeceLabel: {1}".format("Created" if created else "Have", label))

        # Overwrite all fields
        label.info = l["description"]
        label.cece_api_url = "{0}{1}/".format(uri, l["id"])
        label.save()


class Command(CommandWrapper):
    help = "\033[91mUpdate CeceLabels with Cece data, overwriting all fields!\033[0m\n"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_labels
        self.margs = [ self.cmd_name, client ]
        self.mkwargs = { "recursive": not settings.DEBUG }

        super().handle(*args, **options)

