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


def create_or_update_products(logger, cmd_name, client, recursive=True):
    fn = "create_or_update_products"
    client.set_cece_token_headers(logger)

    # Retrieve the (paginated) data
    uri = settings.CECE_API_URI + "mancelot/catalog/product?page_size=1000"
    logger.debug("{0}: GET {1} <-- recursive = {2}".format(fn, uri, recursive))
    data = client.get_list(logger, uri, recursive=recursive)
    logger.debug("{0}: received {1} products".format(fn, len(data)))

    # Get the ContentType pks for the LogEntry
    category_ctpk = ContentType.objects.get_for_model(Category).pk
    subcategory_ctpk = ContentType.objects.get_for_model(Subcategory).pk
    store_ctpk = ContentType.objects.get_for_model(Store).pk
    brand_ctpk = ContentType.objects.get_for_model(Brand).pk
    size_ctpk = ContentType.objects.get_for_model(Size).pk
    color_ctpk = ContentType.objects.get_for_model(Color).pk
    material_ctpk = ContentType.objects.get_for_model(Material).pk
    product_ctpk = ContentType.objects.get_for_model(Product).pk

    # Iterate through the Cece data
    section_map = { v: k for k, v in dict(Category.SECTIONS).items() }
    for i, p in enumerate(data):
        try:
            logger.debug("\n{0} / {1}\n{2}".format(i+1, len(data), p["productID"] ))

            ### Start of brand
            # Related fields: external brand and store are FK, serialized
            #     as string (brand_name, store_name)
            # Get or create Brand. Match on **name** only!
            brand, created = Brand.objects.get_or_create(name=p["brand"])
            logger.debug("  {0} Brand: {1}".format(
                "Created" if created else "Have", brand))

            if created:
                # Log Created to Brand instance only if created
                brand.last_updated_by = client.ceceuser
                LogEntry.objects.log_action(
                    user_id=client.ceceuser.pk,
                    content_type_id=brand_ctpk,
                    object_id=brand.pk,
                    object_repr=str(brand),
                    action_flag=ADDITION,
                    change_message="Created by '{0}'".format(cmd_name)
                )
                brand.save()
            ### End of brand

            ### Start of store
            # Get or create Store. Match on **name** only!
            store, created = Store.objects.get_or_create(name=p["store"])
            logger.debug("  {0} Store: {1}".format(
                "Created" if created else "Have", store))

            if created:
                # Log Created to Store instance only if created
                store.last_updated_by = client.ceceuser
                LogEntry.objects.log_action(
                    user_id=client.ceceuser.pk,
                    content_type_id=store_ctpk,
                    object_id=store.pk,
                    object_repr=str(store),
                    action_flag=ADDITION,
                    change_message="Created by '{0}'".format(cmd_name)
                )
                store.save()
            ### End of store

            ### Start of color
            # Related field: external color is a string (one color per instance)
            # Get or create Color. Match on **name** only!
            color, created = Color.objects.get_or_create(name=p["color"])
            logger.debug("  {0} Color: {1}".format(
                "Created" if created else "Have", color))

            if created:
                # Log Created to Color instance only if created
                color.last_updated_by = client.ceceuser
                LogEntry.objects.log_action(
                    user_id=client.ceceuser.pk,
                    content_type_id=color_ctpk,
                    object_id=color.pk,
                    object_repr=str(color),
                    action_flag=ADDITION,
                    change_message="Created by '{0}'".format(cmd_name)
                )
                color.save()
            ### End of color

            ### Start of product
            # Get or create Product. Match on **cece_id<-->productID** only!
            product_exists = Product.objects.filter( cece_id=p["productID"] ).exists()
            if product_exists:
                product = Product.objects.get( cece_id=p["productID"] )
                created = False
            else:
                product = Product( cece_id=p["productID"] )
                created = True

            # Overwrite all fields
            product.name = p["title"]
            product.info = p["text"]
            product.extra_info = p["extra_text"]
            product.url = p["link"]

            product.price = Money(p["price"], "EUR")
            product.from_price = Money(p["old_price"], "EUR") if p["old_price"] else None

            product.main_image = p["primary_image"]
            product.extra_images = p["extra_images"]
            # TODO: download logo, set url to mancelot.nl
            # TODO: generate thumbnails, max. 10kb

            product.store = store
            product.brand = brand
            product.cece_api_url = "{0}{1}/".format(uri, p["id"])
            product.last_updated_by = client.ceceuser
            product.save()
            logger.debug("  {0} Product: {1}".format("Created" if created else "Have", product))
            # end of fields

            # Log Created/Updated to CeceLabel instance
            LogEntry.objects.log_action(
                user_id=client.ceceuser.pk,
                content_type_id=product_ctpk,
                object_id=product.pk,
                object_repr=str(product),
                action_flag=ADDITION if created else CHANGE,
                change_message="{0} by '{1}'".format(
                    "Created" if created else "Updated", cmd_name
                )
            )
            product.save()


            ### Start of categories
            # Related fields: external category (M2M) and subcategory (FK to category)
            for c in p["category"]:
                c = c.replace("  ", " ")  # 'Underwear &  Socks'
                logger.debug("\n  DEBUG (Cece) c = {0}".format(c))

                # Get or create Category. Match on **name** only!
                category, created = Category.objects.get_or_create(
                    name=c,  # serializes as string (category_name)
                    section=0,  # hard-coded section 'Men'
                )
                logger.debug("  {0} Category: {1} ({2})".format(
                    "Created" if created else "Have", category,
                    category.get_section_display()
                ))

                if created:
                    # Log Created/Updated to Category instance
                    category.last_updated_by = client.ceceuser
                    LogEntry.objects.log_action(
                        user_id=client.ceceuser.pk,
                        content_type_id=category_ctpk,
                        object_id=category.pk,
                        object_repr=str(category),
                        action_flag=ADDITION,
                        change_message="Created by '{0}'".format(cmd_name)
                    )
                    category.save()

                # Add the category to the store, and log to Store instance
                product.categories.add(category)
                LogEntry.objects.log_action(
                    user_id=client.ceceuser.pk,
                    content_type_id=store_ctpk,
                    object_id=store.pk,
                    object_repr=str(store),
                    action_flag=CHANGE,
                    change_message="Category '{0} ({1})' added by '{2}'".format(
                        category.name, category.get_section_display(), cmd_name
                    )
                )
                product.save()
            ### End of categories

            ### Start of subcategories
            for sc in p["subcategory"]:
                logger.debug("\n  DEBUG (Cece) sc = {0}".format(sc["sub_name"]))
                parent, created = Category.objects.get_or_create(
                    name=sc["category"].replace("  ", " "),  # 'Underwear &  Socks'
                    section=0,  # hard-coded section 'Men'
                )
                logger.debug("  {0} (parent) Category: {1} ({2})".format(
                    "Created" if created else "Have", parent,
                    parent.get_section_display()
                ))

                if created:
                    # Log Created/Updated to Category instance
                    parent.last_updated_by = client.ceceuser
                    LogEntry.objects.log_action(
                        user_id=client.ceceuser.pk,
                        content_type_id=category_ctpk,
                        object_id=parent.pk,
                        object_repr=str(parent),
                        action_flag=ADDITION,
                        change_message="Created by '{0}' for Subcategory '{1} ({2})'".format(
                            cmd_name, sc["sub_name"], parent.get_section_display(),
                        )
                    )
                    parent.save()
                # end of parent Category

                # Get or create Subcategory. Match on **(parent) Category** and **name**
                subcategory, created = Subcategory.objects.get_or_create(
                    category=parent,
                    name=sc["sub_name"],
                )
                logger.debug("  {0} Subcategory: {1} ({2})".format(
                    "Created" if created else "Have", subcategory,
                    subcategory.category.get_section_display()
                ))

                if created:
                    # Log Created/Updated to (parent) Category instance
                    subcategory.last_updated_by = client.ceceuser
                    LogEntry.objects.log_action(
                        user_id=client.ceceuser.pk,
                        content_type_id=category_ctpk,
                        object_id=parent.pk,
                        object_repr=str(parent),
                        action_flag=ADDITION,
                        change_message="Subcategory '{0}' added by '{1}'".format(
                            subcategory.name, cmd_name
                        )
                    )
                    subcategory.save()
                    # Log Created/Updated to Subcategory instance
                    subcategory.last_updated_by = client.ceceuser
                    LogEntry.objects.log_action(
                        user_id=client.ceceuser.pk,
                        content_type_id=subcategory_ctpk,
                        object_id=subcategory.pk,
                        object_repr=str(subcategory),
                        action_flag=ADDITION,
                        change_message="Created by '{0}'".format(cmd_name)
                    )
                    subcategory.save()

                # Add the subcategory to the brand, and log to Product instance
                product.subcategories.add(subcategory)
                LogEntry.objects.log_action(
                    user_id=client.ceceuser.pk,
                    content_type_id=product_ctpk,
                    object_id=product.pk,
                    object_repr=str(product),
                    action_flag=CHANGE,
                    change_message="Subcategory '{0} ({1})' added by '{2}'".format(
                        subcategory.name, subcategory.category.get_section_display(),
                        cmd_name
                    )
                )
                product.save()
            ### End of subcategories

            ### Start of material
            for m in p["material"]:
                # Get or created Material. Match on **name** only!
                material, created = Material.objects.get_or_create(
                    name=m,  # serialized as string (name)
                )
                logger.debug("  {0} Material: {1}".format(
                    "Created" if created else "Have", material))
                if created:
                    # Log Created to Material instance only if created
                    material.last_updated_by = client.ceceuser
                    LogEntry.objects.log_action(
                        user_id=client.ceceuser.pk,
                        content_type_id=material_ctpk,
                        object_id=material.pk,
                        object_repr=str(material),
                        action_flag=ADDITION if created else CHANGE,
                        change_message="Created by '{0}'".format(cmd_name),
                    )
                    material.save()

                # Add the material to the product, and log to Product instance
                product.materials.add(material)
                LogEntry.objects.log_action(
                    user_id=client.ceceuser.pk,
                    content_type_id=product_ctpk,
                    object_id=product.pk,
                    object_repr=str(product),
                    action_flag=CHANGE,
                    change_message="Material '{0}' added by '{1}'".format(
                        material.name, cmd_name
                    )
                )
                product.save()
            ### End of material

            ## Start of size
            for s in p["size"]:  # NB external has 'size' singular, but is M2M!
                # Get or create Size. Match on **name** only!
                size, created = Size.objects.get_or_create(
                    name=s,  # serialized as string (name)
                )
                logger.debug("  {0} Size: {1}".format(
                    "Created" if created else "Have", size))

                if created:
                    # Log Created to Size instance only if created
                    size.last_updated_by = client.ceceuser
                    LogEntry.objects.log_action(
                        user_id=client.ceceuser.pk,
                        content_type_id=size_ctpk,
                        object_id=size.pk,
                        object_repr=str(size),
                        action_flag=ADDITION if created else CHANGE,
                        change_message="Created by '{0}'".format(cmd_name),
                    )
                    size.save()

                # Add the size to the product, and log to Product instance
                product.sizes.add(size)
                LogEntry.objects.log_action(
                    user_id=client.ceceuser.pk,
                    content_type_id=product_ctpk,
                    object_id=product.pk,
                    object_repr=str(product),
                    action_flag=CHANGE,
                    change_message="Size '{0}' added by '{1}'".format(
                        size.name, cmd_name
                    )
                )
                product.save()
            ### End of size

            ### End of product
        except Exception as e:
            raise


class Command(CommandWrapper):
    help = "\033[91mUpdate Products with Cece data, overwriting all fields!\033[0m\n"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_products
        self.margs = [ self.cmd_name, client ]
        self.mkwargs = { "recursive": not settings.DEBUG }

        super().handle(*args, **options)

