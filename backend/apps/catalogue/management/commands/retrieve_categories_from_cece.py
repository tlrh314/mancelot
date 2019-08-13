from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry

from catalogue.utils import CeceApiClient
from catalogue.utils import CommandWrapper
from catalogue.models import (
    Category,
    Subcategory,
)


def create_or_update_categories(logger, cmd_name, client):
    fn = "create_or_update_categories"
    client.set_cece_token_headers(logger)

    uri = settings.CECE_API_URI + "mancelot/catalog/category/"
    logger.debug("{0}: GET {1}".format(fn, uri))
    data = client.get_list(logger, uri, recursive=False)
    logger.debug("{0}: received {1} brands".format(fn, len(data)))

    category_ctpk = ContentType.objects.get_for_model(Category).pk
    subcategory_ctpk = ContentType.objects.get_for_model(Subcategory).pk

    logger.debug("\n{0}: create/update".format(fn))
    section_map = { v: k for k, v in dict(Category.SECTIONS).items() }
    for i, c in enumerate(data):
        logger.debug("{0} / {1}".format(i, len(data) ))
        category, created = Category.objects.get_or_create(
            name=c["category_name"],
            section=section_map.get(c["type"], -1),  # TODO: handle data other than Men/Women/Kids
            cece_api_url="{0}{1}/".format(uri, c["id"]),
            last_updated_by=client.ceceuser,
        )
        logger.debug("  {0} Category: {1}".format("Created" if created else "Have", category))
        if created:
            LogEntry.objects.log_action(
                client.ceceuser.pk, category_ctpk, category.pk, str(category), ADDITION,
                change_message="Created by '{0}'".format(cmd_name))
            category.save()

        # Related field: external labels is M2M, serializes as string (name)
        for l in c["subcategory"]:
            cattt = Category.objects.get(name=l["category"])
            print(cattt)
            subcategory, created = Subcategory.objects.get_or_create(
                name=l["sub_name"],
                category=cattt,
                # category=category,  # simpler, aye?
            )
            logger.debug("    {0} Subcategory : {1}".format(
                "Created" if created else "Have", subcategory))
            if created:
                subcategory.last_updated_by = client.ceceuser
                LogEntry.objects.log_action(
                    client.ceceuser.pk, subcategory_ctpk, subcategory.pk, str(subcategory), ADDITION,
                    change_message="Created by '{0}'".format(cmd_name))
                subcategory.save()


class Command(CommandWrapper):
    help = "Update our database with Brand instances from the Cece API"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_categories
        self.margs = [self.cmd_name, client]
        self.mkwargs = {}

        super().handle(*args, **options)

