import factory
from faker import Factory

from catalogue.models import (
    CeceLabel,
    Certificate,
    Category,
    Subcategory,
    PaymentOption,
    Store,
    Brand,
    Size,
    Material,
    Product
)

COLORS = [
    "White",
    "Navy Blue",
    "Grey",
    "Black",
    "Lilac",
    "Green",
    "Other/Multi",
    "Brown",
    "Blue",
    "Beige",
    "Yellow",
    "Red",
    "Pink"
]


faker = Factory.create("nl_NL")


class CeceLabelFactory(factory.DjangoModelFactory):
    class Meta:
        model = CeceLabel

    name = factory.LazyAttribute(lambda _: faker.name())
    info = factory.LazyAttribute(lambda _: faker.text())


class CertificateFactory(factory.DjangoModelFactory):
    class Meta:
        model = Certificate

    name = factory.LazyAttribute(lambda _: faker.name())
    info = factory.LazyAttribute(lambda _: faker.text())


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda _: faker.name())
    section = 0


class SubcategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Subcategory

    name = factory.LazyAttribute(lambda _: faker.name())
    category = factory.SubFactory(CategoryFactory)


class PaymentOptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = PaymentOption

    name = factory.LazyAttribute(lambda _: faker.name())
    logo = "/static/img/test/test_logo.png"


class StoreFactory(factory.DjangoModelFactory):
    class Meta:
        model = Store

    name = factory.LazyAttribute(lambda _: faker.name())
    info = factory.LazyAttribute(lambda _:
        faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
    )
    url = factory.LazyAttribute(lambda _: faker.url())
    logo = "/static/img/test/test_logo.png"
    payment_options = factory.SubFactory(PaymentOptionFactory)

    address = factory.LazyAttribute(lambda _: faker.street_address())
    zip_code = factory.LazyAttribute(lambda _: faker.postcode())
    city = factory.LazyAttribute(lambda _: faker.city())
    # TODO: CountryField instance
    # country = factory.LazyAttribute(lambda _: faker.country())

    @factory.post_generation
    def payment_options(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of PaymentOption instances were passed in, use them
            for pm in extracted:
                self.payment_options.add(pm)


class BrandFactory(factory.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.LazyAttribute(lambda _: faker.name())
    info = factory.LazyAttribute(lambda _:
        faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
    )
    url = factory.LazyAttribute(lambda _: faker.url())
    logo = "/static/img/test/test_logo.png"

    # TODO: add labels and certificates
    # all_labels_random = Label.objects.order_by("?")
    # all_certificates_random = Certificate.objects.order_by("?")
    # for j in range(faker.random_int(min=1, max=all_labels_random.count()-1)):
    #     brand.labels.add(all_labels_random[j])
    # for j in range(faker.random_int(min=0, max=int(all_certificates_random.count()/4))):
    #     brand.certificates.add(all_certificates_random[j])


class SizeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Size

    name = factory.LazyAttribute(lambda _: faker.name())


class MaterialFactory(factory.DjangoModelFactory):
    class Meta:
        model = Material

    name = factory.LazyAttribute(lambda _: faker.name())


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = Product

    @classmethod
    def _generate(cls, strategy, params):
        raise NotImplementedError

    @classmethod
    def _get_or_create(cls, model_class, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        raise NotImplementedError

    name = factory.LazyAttribute(lambda _: faker.name())
    info = factory.LazyAttribute(lambda _:
        faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
    )
    extra_info = factory.LazyAttribute(lambda _:
        faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
    )
    url = factory.LazyAttribute(lambda _: faker.url())

    cece_id = factory.LazyAttribute(lambda _: faker.uuid4()[0:8])

    price = faker.random_int(min=250, max=15000)/100
    # TODO: some fraction of products on sale
    # # assume uniform, 10% should be on sale. Sale price 110-200% of regular price
    # if faker.random_int(min=1, max=100) < 10:
    #     product.old_price = faker.random_int(min=110, max=200)/100 * product.price

    # TODO: may want images we actually have in static
    # main_image
    # extra_images

    # TODO: add valid category
    # product.save()
    # product.category.add(Category.objects.order_by("?").first())
    # TODO: add Subcategory to a fraction of Product instances
    # valid_subcats = product.category.first().subcategory.order_by("?")
    # if valid_subcats:
    #     for j in range(faker.random_int(min=0, max=valid_subcats.count()-1)):
    #         product.subcategory.add(valid_subcats[j])

    # TODO: add the m2m's below
    # brand
    # store
    # material
    # size
    color = factory.LazyAttribute(lambda _:
        COLORS[faker.random_int(min=0, max=len(COLORS)-1)]
    )

