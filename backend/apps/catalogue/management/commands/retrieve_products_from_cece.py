from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from djmoney.money import Money

from catalogue.utils import CeceApiClient
from catalogue.utils import CommandWrapper
from catalogue.models import (
    CeceLabel,
    Certificate,
    Category,
    Subcategory,
    PaymentOption,
    Store,
    Brand,
    Size,
    Color,
    Material,
    Product
)


def create_or_update_products(logger, cmd_name, client, page=""):
    fn = "create_or_update_products"
    client.set_cece_token_headers(logger)

    uri = settings.CECE_API_URI + "mancelot/catalog/product/{0}".format(page)
    logger.debug("{0}: GET {1}".format(fn, uri))
    data = client.get_list(logger, uri, recursive=False)
    logger.debug("{0}: received {1} products".format(fn, len(data)))

    product_ctpk = ContentType.objects.get_for_model(Product).pk

    logger.debug("\n{0}: create/update".format(fn))
    for i, p in enumerate(data):
        try:
            logger.debug("{0} / {1}".format(i, len(data) ))

            # Related fields: external brand and store are FK, serialized
            #     as string (brand_name, store_name)
            brand, created = Brand.objects.get_or_create(name=p["brand"])
            if created:
                brand.last_updated_by = client.ceceuser; brand.save()
            store, created = Store.objects.get_or_create(name=p["store"])
            if created:
                store.last_updated_by = client.ceceuser; store.save()
            # Related field: external color is a string (one color per instance)
            color, created = Color.objects.get_or_create(name=p["color"])
            if created:
                color.last_updated_by = client.ceceuser; color.save()

            product, created = Product.objects.get_or_create(
                name=p["title"],
                info=p["text"],
                extra_info=p["extra_text"],
                url=p["link"],

                cece_id=p["productID"],
                price=Money(p["price"], "EUR"),
                from_price=Money(p["old_price"], "EUR") if p["old_price"] else None,

                main_image=p["primary_image"],
                extra_images=p["extra_images"],

                brand=brand,
                store=store,
                cece_api_url="{0}{1}/".format(uri, p["id"]),
                last_updated_by=client.ceceuser,
            )
            # TODO: download logo, set url to mancelot.nl
            logger.debug("  {0} Product: {1}".format("Created" if created else "Have", product))
            if created:
                LogEntry.objects.log_action(
                    client.ceceuser.pk, product_ctpk, product.pk, str(product), ADDITION,
                    change_message="Created by '{0}'".format(cmd_name))
                product.save()

            # Related fields: external category (M2M) and subcategory (FK to category)
            section_map = { v: k for k, v in dict(Category.SECTIONS).items() }
            for c in p["category"]:
                c = c.replace("  ", " ").strip()  # TODO:  investigate Underwear & Socks
                logger.debug("DEBUG c = {0}".format(c))
                category, created = Category.objects.get_or_create(
                    name=c,  # serializes as string (category_name)
                    section=section_map["Men"],  # NB, this assumes Cece API exclusively offers data in Men section!!!
                )
                if created:
                    category.last_updated_by = client.ceceuser
                    category.save()
                product.categories.add(category)
                product.save()

            for sc in p["subcategory"]:
                parent, created = Category.objects.get_or_create(
                    name=sc["category"].replace("  ", " ").strip()  # TODO: investigate Underwear & Socks
                )
                if created:
                    parent.last_updated_by = client.ceceuser
                    parent.save()
                subcategory, created = Subcategory.objects.get_or_create(
                    category=parent,
                    name=sc["sub_name"],
                )
                if created:
                    subcategory.last_updated_by = client.ceceuser
                    subcategory.save()
                product.subcategories.add(subcategory)
                product.save()

            for m in p["material"]:
                material, created = Material.objects.get_or_create(
                    name=m,  # serialized as string (name)
                )
                if created:
                    material.last_updated_by = client.ceceuser
                    material.save()

                product.materials.add(material)
                product.save()

            for s in p["size"]:  # NB external has 'size' singular, but is M2M!
                size, created = Size.objects.get_or_create(
                    name=s,  # serialized as string (name)
                )
                if created:
                    size.last_updated_by = client.ceceuser
                    size.save()

                product.sizes.add(size)
                product.save()
        except Exception as e:
            # TODO: handle
            continue


class Command(CommandWrapper):
    help = "Update our database with Product instances from the Cece API"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_products
        self.margs = [self.cmd_name, client]
        self.mkwargs = {"page": "?page=4"}

        super().handle(*args, **options)

