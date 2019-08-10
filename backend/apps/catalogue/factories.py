import factory
from faker import Factory
from django.conf import settings
from django_countries import countries

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


faker = Factory.create("nl_NL")
COLORS = list()
while len(COLORS) < 60:
    c = faker.color_name()
    if c not in COLORS: COLORS.append(c)

SIZES = [ "3XS", "XXS", "XS", "S", "M", "L", "XL", "XXL", "3XL", "4XL"] + \
    ["UK {0}".format(i) for i in range(4, 30, 2)] + \
    ["FR {0}".format(i) for i in range(32, 58, 2)] + \
    ["EU {0}".format(i) for i in range(40, 52, 2)]


class CeceLabelFactory(factory.DjangoModelFactory):
    class Meta:
        model = CeceLabel
        django_get_or_create = ("name",)

    name = factory.LazyAttribute(lambda _: faker.name())
    info = factory.LazyAttribute(lambda _: faker.text())


class CertificateFactory(factory.DjangoModelFactory):
    class Meta:
        model = Certificate
        django_get_or_create = ("name",)

    name = factory.LazyAttribute(lambda _: faker.name())
    info = factory.LazyAttribute(lambda _: faker.text())


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = factory.LazyAttribute(lambda _: faker.name())
    section = 0

    @factory.post_generation
    def subcategories(self, create, extracted, **kwargs):
        # ForeignKey relation at Subcategory. Here we use the related_name
        if not create or kwargs.get("skip"):
            return

        if extracted:
            for subcategory in extracted:
                self.subcategories.add(extracted)
            return

        for i in range(faker.random_int(min=0, max=10)):
            self.subcategories.add(Subcategory.objects.create(
                name="{0}: Sub {1}".format(self.name, i),
                category=self)
            )


class SubcategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Subcategory
        django_get_or_create = ("name",)

    name = factory.LazyAttribute(lambda _: faker.name())

    # We do not want CategoryFactory.subcategories post_generation to add any
    # subcategories (which it does by default), but we cannot use the extracted
    # block either because we would have to give 'self', i.e. the Subcategory
    # that we create in this factory (and bool empty QuerySet is False). We
    # cannot use post_generation on the SubcategoryFactory either because that
    # is executed after save, and category_id cannot be none on save.
    # So we pass skip=True as kwarg to the subcategories post_generation
    # method such that the category does not generate subcategories, but
    # it is added to this subcategory :-).
    category = factory.SubFactory(CategoryFactory, subcategories__skip=True)


class PaymentOptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = PaymentOption
        django_get_or_create = ("name",)

    name = factory.LazyAttribute(lambda _: faker.name())
    logo = "/static/img/test/test_logo.png"


class StoreFactory(factory.DjangoModelFactory):
    class Meta:
        model = Store
        django_get_or_create = ("name",)

    name = factory.LazyAttribute(lambda _: faker.company())
    info = factory.LazyAttribute(lambda _:
        faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
    )
    url = factory.LazyAttribute(lambda _: faker.url())
    logo = "/static/img/test/test_logo.png"

    address = factory.LazyAttribute(lambda _: faker.street_address())
    zip_code = factory.LazyAttribute(lambda _: faker.postcode())
    city = factory.LazyAttribute(lambda _: faker.city())
    country = "NL"  # alternatively, use code below to randomly select
    # country = factory.LazyAttribute(lambda _:
    #     list(countries)[faker.random_int(min=0, max=len(countries)-1)][0]  # ('NL', 'Nederland')
    # )

    # Add zero up to all payment_options (number of payment_options is randomly selected)
    @factory.post_generation
    def payment_options(self, create, extracted, **kwargs):
        if not create or kwargs.get("skip"):
            return

        if extracted:
            for payment_option in extracted:
                self.payment_option.add(label)
            return

        # Create CeceLabel instances if there are less than fifteen available
        if PaymentOption.objects.count() < 15:
            PaymentOptionFactory.create_batch(15 - PaymentOption.objects.count())

        number_of_payment_options_to_add = faker.random_int(min=0, max=PaymentOption.objects.count()-1)
        all_payment_options_randomly_ordered = PaymentOption.objects.order_by("?")
        for j in range(number_of_payment_options_to_add):
            self.payment_options.add(all_payment_options_randomly_ordered[j])


class BrandFactory(factory.DjangoModelFactory):
    class Meta:
        model = Brand
        django_get_or_create = ("name",)

    name = factory.LazyAttribute(lambda _: faker.company())
    info = factory.LazyAttribute(lambda _:
        faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
    )
    url = factory.LazyAttribute(lambda _: faker.url())
    logo = "/static/img/test/test_logo.png"

    # Add zero up to all labels (number of labels is randomly selected)
    @factory.post_generation
    def labels(self, create, extracted, **kwargs):
        if not create or kwargs.get("skip"):
            return

        if extracted:
            for label in extracted:
                self.labels.add(label)
            return

        # Create CeceLabel instances if there are less than five labels available
        if CeceLabel.objects.count() < 5:
            CeceLabelFactory.create_batch(5 - CeceLabel.objects.count())

        number_of_labels_to_add = faker.random_int(min=0, max=CeceLabel.objects.count()-1)
        all_labels_randomly_ordered = CeceLabel.objects.order_by("?")
        for j in range(number_of_labels_to_add):
            self.labels.add(all_labels_randomly_ordered[j])

    # Add zero up to 25% of certificates (number of certificates is randomly selected)
    @factory.post_generation
    def certificates(self, create, extracted, **kwargs):
        if not create or kwargs.get("skip"):
            return

        if extracted:
            for certificate in extracted:
                self.certificates.add(certificate)
            return

        # Create Certificate instances if there are less than twenty available
        if Certificate.objects.count() < 20:
            CertificateFactory.create_batch(20 - Certificate.objects.count())

        number_of_certificates_to_add = faker.random_int(
            min=0, max=int(0.25*Certificate.objects.count()))
        all_certificates_randomly_ordered = Certificate.objects.order_by("?")
        for j in range(number_of_certificates_to_add):
            self.certificates.add(all_certificates_randomly_ordered[j])


class SizeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Size
        django_get_or_create = ("name",)

    name = factory.LazyAttribute(lambda _:
        SIZES[faker.random_int(min=0, max=len(SIZES)-1)]
    )

class ColorFactory(factory.DjangoModelFactory):
    class Meta:
        model = Color
        django_get_or_create = ("name",)

    name = factory.LazyAttribute(lambda _:
        COLORS[faker.random_int(min=0, max=len(COLORS)-1)]
    )


class MaterialFactory(factory.DjangoModelFactory):
    class Meta:
        model = Material
        django_get_or_create = ("name",)

    name = factory.LazyAttribute(lambda _: faker.word())


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ("name",)

    name = factory.LazyAttribute(lambda _: faker.name())
    info = factory.LazyAttribute(lambda _:
        faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
    )
    extra_info = factory.LazyAttribute(lambda _:
        faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
    )
    url = factory.LazyAttribute(lambda _: faker.url())

    cece_id = factory.LazyAttribute(lambda _: faker.uuid4()[0:8])

    price = factory.LazyAttribute(lambda _:
        faker.random_int(min=250, max=15000)/100
    )
    @factory.post_generation
    def from_price(self, create, extracted, **kwargs):
        if not create or kwargs.get("skip"):
            return

        if extracted:
            self.from_price = extracted
            return

        # assume uniform, 20% should be on sale. Sale price 120-250% of regular price
        if faker.random_int(min=0, max=100) < 20:
            self.from_price = faker.random_int(min=120, max=250)/100 * self.price

    main_image = factory.LazyAttribute(lambda _:
        "{0}/img/test/cat{1}.jpg".format(
            settings.STATIC_ROOT, faker.random_int(min=1, max=30)
        )
    )
    @factory.post_generation
    def extra_images(self, create, extracted, **kwargs):
        if not create or kwargs.get("skip"):
            return

        if extracted:
            self.extra_images = extracted
            return

        self.extra_images = []
        for i in range(faker.random_int(min=0, max=5)):
            img = "{0}/img/test/cat{1}.jpg".format(
                settings.STATIC_ROOT, faker.random_int(min=1, max=30)
            )
            if img not in self.extra_images: self.extra_images.append(img)

    # Create Brand instances if there are less than fourty brands available
    # NB, this code might also execute on import. Not sure if that's desired
    # TODO: decide on how to sample brand
    if Brand.objects.count() < 40:
        BrandFactory.create_batch(40 - Brand.objects.count())
    brand = Brand.objects.order_by("?").first()

    # Hmm the line below spawns a new Brand for each ProductFactory call, wops
    # brand = factory.SubFactory(
    #     BrandFactory, labels__skip=True, certificates__skip=True
    # )

    # Create Store instances if there are less than twenty brands available
    # NB, this code might also execute on import. Not sure if that's desired
    # TODO: decide on how to sample store
    if Store.objects.count() < 20:
        StoreFactory.create_batch(20 - Store.objects.count())
    store = Store.objects.order_by("?").first()

    # Hmm the line below spawns a new Store for each ProductFactory call, wops
    # store = factory.SubFactory(StoreFactory, payment_options__skip=True)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):  # M2M relation
        if not create or kwargs.get("skip"):
            return

        if extracted:
            for category in extracted:
                self.categories.add(category)
            return

        # Create Category instances if there are less than twenty-five categories available
        if Category.objects.count() < 25:
            CategoryFactory.create_batch(25 - Category.objects.count())

        number_of_categories_to_add = faker.random_int(min=0, max=Category.objects.count()-1)
        all_categories_randomly_ordered = Category.objects.order_by("?")
        for j in range(number_of_categories_to_add):
            self.categories.add(all_categories_randomly_ordered[j])

    @factory.post_generation
    def subcategories(self, create, extracted, **kwargs):
        if not create or kwargs.get("skip"):
            return

        if extracted:
            for category in extracted:
                self.categories.add(category)
            return

        # Create Subcategory instances if there are less than twenty-five available
        if Subcategory.objects.count() < 25:
            SubcategoryFactory.create_batch(25 - Subcategory.objects.count())

        number_of_categories_to_add = faker.random_int(min=0, max=Subcategory.objects.count()-1)
        all_categories_randomly_ordered = Subcategory.objects.order_by("?")
        for j in range(number_of_categories_to_add):
            self.subcategories.add(all_categories_randomly_ordered[j])

    @factory.post_generation
    def materials(self, create, extracted, **kwargs):
        if not create or kwargs.get("skip"):
            return

        if extracted:
            for material in extracted:
                self.materials.add(material)
            return

        # Create Material instances if there are less than twenty-five available
        if Material.objects.count() < 25:
            MaterialFactory.create_batch(25 - Material.objects.count())

        number_of_materials_to_add = faker.random_int(min=0, max=Material.objects.count()-1)
        all_materials_randomly_ordered = Material.objects.order_by("?")
        for j in range(number_of_materials_to_add):
            self.materials.add(all_materials_randomly_ordered[j])

    @factory.post_generation
    def sizes(self, create, extracted, **kwargs):
        if not create or kwargs.get("skip"):
            return

        if extracted:
            for size in extracted:
                self.sizes.add(size)
            return

        # Create Size instances if there are less than twenty-five sizes available
        if Size.objects.count() < 25:
            SizeFactory.create_batch(25 - Size.objects.count())

        number_of_sizes_to_add = faker.random_int(min=0, max=Size.objects.count()-1)
        all_sizes_randomly_ordered = Size.objects.order_by("?")
        for j in range(number_of_sizes_to_add):
            self.sizes.add(all_sizes_randomly_ordered[j])

    @factory.post_generation
    def colors(self, create, extracted, **kwargs):
        if not create or kwargs.get("skip"):
            return

        if extracted:
            for color in extracted:
                self.colors.add(color)
            return

        # Create Color instances if there are less than twenty-five available
        if Color.objects.count() < 25:
            ColorFactory.create_batch(25 - Color.objects.count())

        number_of_colors_to_add = faker.random_int(min=0, max=Color.objects.count()-1)
        all_colors_randomly_ordered = Color.objects.order_by("?")
        for j in range(number_of_colors_to_add):
            self.colors.add(all_colors_randomly_ordered[j])
