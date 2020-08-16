import os
import hashlib
import requests
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from djmoney.money import Money

from catalogue.utils import (
    call_download_image,
    generate_thumbnail,
    optimize_image,
    CeceApiClient,
    CommandWrapper,
)
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

def get_or_create_brand(logger, p, brand_ctpk, client, cmd_name):
    """ Get or create Brand. Match on **name** only! """

    brand, created = Brand.objects.get_or_create(name=p["brand"])
    logger.debug("  {0} Brand: {1}".format(
        "Created" if created else "Have", brand))

    return brand


def get_or_create_store(logger, p, store_ctpk, client, cmd_name):
    """ Get or create Store. Match on **name** only! """

    store, created = Store.objects.get_or_create(name=p["store"])
    logger.debug("  {0} Store: {1}".format(
        "Created" if created else "Have", store))

    return store


def get_or_create_color(logger, p, product, product_ctpk,
        color_ctpk, client, cmd_name):

    """ Get or create Color. Match on **name** only! """

    color, created = Color.objects.get_or_create(name=p["color"])
    logger.debug("  {0} Color: {1}".format(
        "Created" if created else "Have", color))

    product.colors.add(color)
    product.save()


def get_or_create_categories(logger, p, product, product_ctpk,
        category_ctpk, client, cmd_name):

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

        product.categories.add(category)
        product.save()


def get_or_create_subcategories(logger, p, product, product_ctpk,
        category_ctpk, subcategory_ctpk, client, cmd_name):

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

       # Add the subcategory to the brand
       product.subcategories.add(subcategory)
       product.save()


def get_or_create_material(logger, p, product, product_ctpk,
        material_ctpk, client, cmd_name):
    """ Get or created Material. Match on **name** only! """

    for m in p["material"]:
        material, created = Material.objects.get_or_create(
            name=m,  # serialized as string (name)
        )
        logger.debug("  {0} Material: {1}".format(
            "Created" if created else "Have", material))

        # Add the material to the product
        product.materials.add(material)
        product.save()


def get_or_create_size(logger, p, product, product_ctpk,
        size_ctpk, client, cmd_name):

    """ Get or create Size. Match on **name** only! """

    for s in p["size"]:  # NB external has 'size' singular, but is M2M!
        size, created = Size.objects.get_or_create(
            name=s,  # serialized as string (name)
        )
        logger.debug("  {0} Size: {1}".format(
            "Created" if created else "Have", size))

        product.sizes.add(size)
        product.save()


def create_or_update_products(logger, cmd_name, client, recursive=True):
    fn = "create_or_update_products"
    client.set_cece_token_headers(logger)

    # Retrieve the (paginated) data
    uri = settings.CECE_API_URI + "mancelot/catalog/product?page_size=1000"
    logger.debug("{0}: GET {1} <-- recursive = {2}".format(fn, uri, recursive))
    data = client.get_list(logger, uri, recursive=recursive)
    logger.debug("{0}: received {1} products".format(fn, len(data)))

    # Iterate through the Cece data
    section_map = { v: k for k, v in dict(Category.SECTIONS).items() }
    for i, p in enumerate(data):
        try:
            logger.debug("\n{0} / {1}\n{2}".format(i+1, len(data), p["productID"] ))

            # Related fields: external brand and store are FK, serialized
            #     as string (brand_name, store_name)
            brand = get_or_create_brand(logger, p, brand_ctpk, client, cmd_name)
            store = get_or_create_store(logger, p, store_ctpk, client, cmd_name)

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

            # product.main_image and product.extra_images all the way at the end

            product.store = store
            product.brand = brand
            product.cece_api_url = "{0}{1}/".format(uri, p["id"])
            product.last_updated_by = client.ceceuser
            product.save()
            logger.debug("  {0} Product: {1}".format("Created" if created else "Have", product))
            # end of fields

            # Related field: external color is a string (one color per instance)
            get_or_create_color(logger, p, product, product_ctpk,
                color_ctpk, client, cmd_name)

            # Related fields: external category (M2M) and subcategory (FK to category)
            get_or_create_categories(logger, p, product, product_ctpk,
                category_ctpk, client, cmd_name)
            get_or_create_subcategories(logger, p, product, product_ctpk,
                category_ctpk, subcategory_ctpk, client, cmd_name)
            get_or_create_material(logger, p, product, product_ctpk,
                material_ctpk, client, cmd_name)
            get_or_create_size(logger, p, product, product_ctpk,
                size_ctpk, client, cmd_name)
            ### End of product

            ### Download the images.
            extra_images = p["extra_images"].replace("[", "").replace("]", ""
                ).replace("'", "").split(", ")  # p["extra_images"] is str, and json.loads fails

            # Create folder if it does not exist
            img_dir = "{0}/img/products/{1}".format(
                settings.STATIC_ROOT, store.slug
            )
            if not os.path.exists(img_dir) or not os.path.isdir(img_dir):
                os.makedirs(img_dir)
                logger.debug("  Created folder '{0}'".format(img_dir))

            # Iterate through all images
            all_extra_images = []
            for i, img_url in enumerate([ p["primary_image"] ] + extra_images):
                if not img_url: continue
                fname = os.path.basename(urlparse(img_url).path)
                logger.debug("  Fetch '{0}' from Cece".format(img_url))
                if "cece" not in img_url:
                    if img_url.startswith("//"):
                        img_url = img_url.replace("//", "https://")
                    headers = { "user-agent": "Mancelot Bot v1.3.3.7" }
                    response = requests.head(img_url, headers=headers)
                    if response.status_code != 200:
                        logger.error("    Could not retrieve img_url = '{0}'.".format(img_url))
                        continue
                    extension = response.headers["Content-Type"].replace("image/", "")
                    fname = "{0}.{1}".format(
                        hashlib.md5(img_url.encode("utf-8")).hexdigest()[0:7],
                        extension
                    )

                save_to = "{0}/img/products/{1}/{2}".format(
                    settings.STATIC_ROOT, store.slug, fname
                )
                download_success = call_download_image(logger, img_url, save_to,
                    product, "main_image" if i is 0 else "extra_images",
                    product_ctpk, client.ceceuser.pk, cmd_name
                )
                logger.debug("    download_success: {0}".format(download_success))
                if download_success:
                    for size in [(64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)]:
                        # generate_thumbnail also calls optimize_image on thumb
                        generate_thumbnail(logger, save_to, size=size, w="    ")

                    if i > 0:
                        # b/c set to single image above
                        all_extra_images.append(product.extra_images)

            thumbnail = product.main_image.replace(".jpg", "_256x256.jpg")
            thumbnail_path = "{0}/{1}".format(
                str(settings.STATIC_ROOT),
                urlparse(thumbnail).path
            ).replace("//static", "")
            if os.path.exists(thumbnail_path) and os.path.isfile(thumbnail_path):
                product.thumbnail = thumbnail
                product.save()
            product.extra_images = all_extra_images
            product.save()
            ### End of logo download
        except Exception as e:
            # Pushes to Sentry
            logger.error("Caught error in '{0}': {1}".format(cmd_name, e))


class Command(CommandWrapper):
    help = "\033[91mUpdate Products with Cece data, overwriting all fields!\033[0m\n"

    def handle(self, *args, **options):
        client = CeceApiClient()
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = create_or_update_products
        self.margs = [ self.cmd_name, client ]
        self.mkwargs = { "recursive": not settings.DEBUG }

        super().handle(*args, **options)
