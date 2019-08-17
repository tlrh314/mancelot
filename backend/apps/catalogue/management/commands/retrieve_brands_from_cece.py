from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry

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

    # Get the ContentType pks for the LogEntry
    brand_ctpk = ContentType.objects.get_for_model(Brand).pk
    label_ctpk = ContentType.objects.get_for_model(CeceLabel).pk
    certificate_ctpk = ContentType.objects.get_for_model(Certificate).pk

    # Iterate through the Cece data
    for i, b in enumerate(data):
        logger.debug("\n{0} / {1}".format(i+1, len(data) ))

        # Get or create Brand. Match on **name** only!
        brand, created = Brand.objects.get_or_create(
            name=b["brand_name"],
        )
        logger.debug("{0} Brand: {1}".format(
            "Created" if created else "Updated", brand))

        # Overwrite all fields
        brand.info = b["about_brand"]
        brand.cece_api_url = "{0}{1}/".format(uri, b["id"])
        brand.last_updated_by = client.ceceuser

        # Log Created/Updated to Brand instance
        LogEntry.objects.log_action(
            user_id=client.ceceuser.pk,
            content_type_id=brand_ctpk,
            object_id=brand.pk,
            object_repr=str(brand),
            action_flag=ADDITION if created else CHANGE,
            change_message="{0} by '{1}'".format(
                "Created" if created else "Updated", cmd_name
            )
        )
        brand.save()

        # Related field: external labels is M2M, serializes as string (name)
        for l in b["labels"]:
            # Get or create CeceLabel. Match on **name** only!
            label, created = CeceLabel.objects.get_or_create(name=l["label_name"])
            logger.debug("  {0} CeceLabel: {1}".format(
                "Created" if created else "Have", label))

            if created:
                # Log Created to CeceLabel instance only if created
                label.last_updated_by = client.ceceuser
                LogEntry.objects.log_action(
                    user_id=client.ceceuser.pk,
                    content_type_id=label_ctpk,
                    object_id=label.pk,
                    object_repr=str(label),
                    action_flag=ADDITION if created else CHANGE,
                    change_message="Created by '{0}'".format(cmd_name),
                )
                label.save()

            # Add the label to the brand, and log to Brand instance
            brand.labels.add(label)
            LogEntry.objects.log_action(
                user_id=client.ceceuser.pk,
                content_type_id=brand_ctpk,
                object_id=brand.pk,
                object_repr=str(brand),
                action_flag=CHANGE,
                change_message="CeceLabel '{0}' added by '{1}'".format(
                    label.name, cmd_name
                )
            )
            brand.save()

        # Related field: external labels is M2M, serializes as string (name)
        for c in b["certificate"]:
            # Get or create Certificate. Match on **name** only!
            certificate, created = Certificate.objects.get_or_create(name=c)
            logger.debug("  {0} Certificate: {1}".format(
                "Created" if created else "Have", certificate))

            if created:
                # Log Created to Certificate instance only if created
                certificate.last_updated_by = client.ceceuser
                LogEntry.objects.log_action(
                    user_id=client.ceceuser.pk,
                    content_type_id=certificate_ctpk,
                    object_id=certificate.pk,
                    object_repr=str(certificate),
                    action_flag=ADDITION if created else CHANGE,
                    change_message="{0} by '{1}'".format(
                        "Created" if created else "Updated", cmd_name
                    )
                )

            # Add the certificate to the brand, and log to Brand instance
            brand.certificates.add(certificate)
            LogEntry.objects.log_action(
                user_id=client.ceceuser.pk,
                content_type_id=brand_ctpk,
                object_id=brand.pk,
                object_repr=str(brand),
                action_flag=CHANGE,
                change_message="Certificate '{0}' added by '{1}'".format(
                    certificate.name, cmd_name
                )
            )
            brand.save()


class Command(CommandWrapper):
    help = "\033[91mUpdate Brands with Cece data, overwriting all fields!\033[0m\n"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_brands
        self.margs = [ self.cmd_name, client ]
        self.mkwargs = { "recursive": not settings.DEBUG }

        super().handle(*args, **options)
