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


def create_or_update_brands(logger, cmd_name, client):
    fn = "create_or_update_brands"
    client.set_cece_token_headers(logger)

    uri = settings.CECE_API_URI + "mancelot/catalog/brand/"
    logger.debug("{0}: GET {1}".format(fn, uri))
    data = client.get_list(logger, uri, recursive=True)
    logger.debug("{0}: received {1} brands".format(fn, len(data)))

    brand_ctpk = ContentType.objects.get_for_model(Brand).pk
    label_ctpk = ContentType.objects.get_for_model(CeceLabel).pk
    certificate_ctpk = ContentType.objects.get_for_model(Certificate).pk

    logger.debug("\n{0}: create/update".format(fn))
    for i, b in enumerate(data):
        logger.debug("{0} / {1}".format(i, len(data) ))
        brand, created = Brand.objects.get_or_create(
            name=b["brand_name"],
            info=b["about_brand"],
            cece_api_url="{0}{1}/".format(uri, b["id"]),
            last_updated_by=client.ceceuser,
        )
        logger.debug("  {0} Brand: {1}".format("Created" if created else "Have", brand))
        if created:
            LogEntry.objects.log_action(
                client.ceceuser.pk, brand_ctpk, brand.pk, str(brand), ADDITION,
                change_message="Created by '{0}'".format(cmd_name))
            brand.save()

        # Related field: external labels is M2M, serializes as string (name)
        for l in b["labels"]:
            label, created = CeceLabel.objects.get_or_create(name=l)  # TODO: Cece serializer gives abbreviation, not name
            logger.debug("    {0} CeceLabel: {1}".format(
                "Created" if created else "Have", label))
            if created:
                label.last_updated_by = client.ceceuser
                LogEntry.objects.log_action(
                    client.ceceuser.pk, label_ctpk, label.pk, str(label), ADDITION,
                    change_message="Created by '{0}'".format(cmd_name))
                label.save()
            brand.labels.add(label); brand.save()

        # Related field: external labels is M2M, serializes as string (name)
        for c in b["certificate"]:
            certificate, created = Certificate.objects.get_or_create(name=c)
            logger.debug("    {0} Certificate: {1}".format(
                "Created" if created else "Have", certificate))
            if created:
                certificate.last_updated_by = client.ceceuser
                certificate.save()
                LogEntry.objects.log_action(
                    client.ceceuser.pk, certificate_ctpk, certificate.pk, str(certificate), ADDITION,
                    change_message="Created by '{0}'".format(cmd_name))
                certificate.save()
            brand.certificates.add(certificate); certificate.save()


class Command(CommandWrapper):
    help = "Update our database with Brand instances from the Cece API"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_brands
        self.margs = [self.cmd_name, client]
        self.mkwargs = {}

        super().handle(*args, **options)

