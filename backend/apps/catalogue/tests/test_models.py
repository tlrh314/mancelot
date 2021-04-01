from faker import Faker
from django.test import TestCase
from django.utils import translation
from django.utils.text import slugify
from django.core.exceptions import ValidationError

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
    Product,
)
from catalogue.factories import (
    CeceLabelFactory,
    CertificateFactory,
    CategoryFactory,
    SubcategoryFactory,
    PaymentOptionFactory,
    StoreFactory,
    BrandFactory,
    SizeFactory,
    ColorFactory,
    MaterialFactory,
    ProductFactory,
)


faker = Faker()


class CeceLabelTest(TestCase):
    def test_verbose_name(self):
        translation.activate("en")
        self.assertEqual(str(CeceLabel._meta.verbose_name), "Label")
        self.assertEqual(str(CeceLabel._meta.verbose_name_plural), "Labels")
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_string_representation(self):
        obj = CeceLabel(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        translation.activate("en")
        self.assertEqual(CeceLabel._meta.get_field("name").verbose_name, "name")
        self.assertEqual(CeceLabel._meta.get_field("slug").verbose_name, "slug")
        self.assertEqual(CeceLabel._meta.get_field("info").verbose_name, "info")

        self.assertEqual(
            CeceLabel._meta.get_field("date_created").verbose_name, "date created"
        )
        self.assertEqual(
            CeceLabel._meta.get_field("date_updated").verbose_name, "date updated"
        )
        self.assertEqual(
            CeceLabel._meta.get_field("last_updated_by").verbose_name, "last updated by"
        )
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_required_name_not_given_fails(self):
        pass

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = CeceLabelFactory(name=name)
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_absolute_url(self):
        pass

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        pass


class CertificateTest(TestCase):
    def test_verbose_name(self):
        translation.activate("en")
        self.assertEqual(str(Certificate._meta.verbose_name), "Certificate")
        self.assertEqual(str(Certificate._meta.verbose_name_plural), "Certificates")
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_string_representation(self):
        obj = Certificate(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        translation.activate("en")
        self.assertEqual(Certificate._meta.get_field("name").verbose_name, "name")
        self.assertEqual(Certificate._meta.get_field("slug").verbose_name, "slug")
        self.assertEqual(Certificate._meta.get_field("info").verbose_name, "info")
        # TODO: self.assertEqual(Certificate._meta.get_field("url").verbose_name, "url")

        self.assertEqual(
            Certificate._meta.get_field("date_created").verbose_name, "date created"
        )
        self.assertEqual(
            Certificate._meta.get_field("date_updated").verbose_name, "date updated"
        )
        self.assertEqual(
            Certificate._meta.get_field("last_updated_by").verbose_name,
            "last updated by",
        )
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_required_name_not_given_fails(self):
        pass

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = CertificateFactory(name=name)
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_absolute_url(self):
        pass

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        pass


class CategoryTest(TestCase):
    def test_verbose_name(self):
        translation.activate("en")
        self.assertEqual(str(Category._meta.verbose_name), "Category")
        self.assertEqual(str(Category._meta.verbose_name_plural), "Categories")
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_string_representation(self):
        obj = Category(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        translation.activate("en")
        self.assertEqual(Category._meta.get_field("name").verbose_name, "name")
        self.assertEqual(Category._meta.get_field("slug").verbose_name, "slug")
        self.assertEqual(Category._meta.get_field("section").verbose_name, "section")

        self.assertEqual(
            Category._meta.get_field("date_created").verbose_name, "date created"
        )
        self.assertEqual(
            Category._meta.get_field("date_updated").verbose_name, "date updated"
        )
        self.assertEqual(
            Category._meta.get_field("last_updated_by").verbose_name, "last updated by"
        )
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_required_name_not_given_fails(self):
        pass

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = CategoryFactory(name=name)
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        pass

    def test_default_section(self):
        obj = Category()
        self.assertEqual(obj.section, 0)

    def test_category_subcategory_creation(self):
        # If tests run in parallel this test could fail because database content
        # might have changed ..
        ncat_pre = Category.objects.count()
        category = Category.objects.create(name="Ondergoed & Sokken")
        nsubcat_pre = Subcategory.objects.count()
        subcategory1 = Subcategory.objects.create(name="Ondergoed", category=category)
        subcategory2 = Subcategory.objects.create(name="Sokken", category=category)

        self.assertEqual(Category.objects.count(), ncat_pre + 1)
        self.assertEqual(Subcategory.objects.count(), nsubcat_pre + 2)
        self.assertEqual(Subcategory.objects.count(), nsubcat_pre + 2)
        self.assertEqual(category.subcategories.all(), nsubcat_pre + 2)
        self.assertEqual(category.subcategories.all()[-2], subcategory1)
        self.assertEqual(category.subcategories.all()[-1], subcategory2)
        self.assertEqual(subcategory1.category, category)
        self.assertEqual(subcategory2.category, category)
        # Delete manually on purpose. Below we test CASCADE
        subcategory2.delete()
        subcategory1.delet()
        category.delete()

    def test_delete_cascades_down_to_foreign_key_subcategory_deletion(self):
        ncat_pre = Category.objects.count()
        category = Category.objects.create(name="Ondergoed & Sokken")
        nsubcat_pre = Subcategory.objects.count()
        subcategory1 = Subcategory.objects.create(name="Ondergoed", category=category)
        subcategory2 = Subcategory.objects.create(name="Sokken", category=category)

        self.assertEqual(Category.objects.count(), ncat_pre + 1)
        self.assertEqual(Subcategory.objects.count(), nsubcat_pre + 2)
        self.assertEqual(Subcategory.objects.count(), nsubcat_pre + 2)

        # Now delete
        category.delete()
        self.assertEqual(Category.objects.count(), ncat_pre)
        self.assertEqual(Subcategory.objects.count(), nsubcat_pre)
        self.assertEqual(Subcategory.objects.count(), nsubcat_pre)


class SubcategoryTest(TestCase):
    def test_verbose_name(self):
        translation.activate("en")
        self.assertEqual(str(Subcategory._meta.verbose_name), "Subcategory")
        self.assertEqual(str(Subcategory._meta.verbose_name_plural), "Subcategories")
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_string_representation(self):
        obj = Subcategory(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        translation.activate("en")
        self.assertEqual(Subcategory._meta.get_field("name").verbose_name, "name")
        self.assertEqual(Subcategory._meta.get_field("slug").verbose_name, "slug")
        self.assertEqual(
            Subcategory._meta.get_field("category").verbose_name, "category"
        )

        self.assertEqual(
            Subcategory._meta.get_field("date_created").verbose_name, "date created"
        )
        self.assertEqual(
            Subcategory._meta.get_field("date_updated").verbose_name, "date updated"
        )
        self.assertEqual(
            Subcategory._meta.get_field("last_updated_by").verbose_name,
            "last updated by",
        )
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_required_name_not_given_fails(self):
        pass

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = SubcategoryFactory(name=name)  # which creates category too
        self.assertEqual(obj.slug, slugify(name))
        category = obj.category
        obj.delete()
        category.delete()  # because SET_NULL

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        pass


class PaymentOptionTest(TestCase):
    def test_verbose_name(self):
        translation.activate("en")
        self.assertEqual(str(PaymentOption._meta.verbose_name), "PaymentOption")
        self.assertEqual(str(PaymentOption._meta.verbose_name_plural), "PaymentOptions")
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_string_representation(self):
        obj = PaymentOption(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        translation.activate("en")
        self.assertEqual(PaymentOption._meta.get_field("name").verbose_name, "name")
        self.assertEqual(PaymentOption._meta.get_field("slug").verbose_name, "slug")
        self.assertEqual(PaymentOption._meta.get_field("logo").verbose_name, "logo")

        self.assertEqual(
            PaymentOption._meta.get_field("date_created").verbose_name, "date created"
        )
        self.assertEqual(
            PaymentOption._meta.get_field("date_updated").verbose_name, "date updated"
        )
        self.assertEqual(
            PaymentOption._meta.get_field("last_updated_by").verbose_name,
            "last updated by",
        )
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_required_name_not_given_fails(self):
        pass

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = PaymentOptionFactory(name=name)
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_absolute_url(self):
        pass

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        pass

    def test_logo_upload(self):
        pass


class StoreTest(TestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

    def test_verbose_name(self):
        translation.activate("en")
        self.assertEqual(str(Store._meta.verbose_name), "Store")
        self.assertEqual(str(Store._meta.verbose_name_plural), "Stores")
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_string_representation(self):
        obj = Store(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        translation.activate("en")
        self.assertEqual(Store._meta.get_field("name").verbose_name, "name")
        self.assertEqual(Store._meta.get_field("slug").verbose_name, "slug")
        self.assertEqual(Store._meta.get_field("info").verbose_name, "info")
        self.assertEqual(Store._meta.get_field("url").verbose_name, "url")
        self.assertEqual(Store._meta.get_field("logo").verbose_name, "logo")
        self.assertEqual(
            Store._meta.get_field("payment_options").verbose_name, "payment options"
        )
        self.assertEqual(Store._meta.get_field("address").verbose_name, "address")
        self.assertEqual(Store._meta.get_field("zip_code").verbose_name, "zip code")
        self.assertEqual(Store._meta.get_field("city").verbose_name, "city")
        self.assertEqual(Store._meta.get_field("country").verbose_name, "country")

        self.assertEqual(
            Store._meta.get_field("date_created").verbose_name, "date created"
        )
        self.assertEqual(
            Store._meta.get_field("date_updated").verbose_name, "date updated"
        )
        self.assertEqual(
            Store._meta.get_field("last_updated_by").verbose_name, "last updated by"
        )
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_required_name_not_given_fails(self):
        pass

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = StoreFactory(name=name)
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        pass

    def test_logo_upload(self):
        pass

    def test_payment_options(self):
        pass


class BrandTest(TestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

    def test_verbose_name(self):
        translation.activate("en")
        self.assertEqual(str(Brand._meta.verbose_name), "Brand")
        self.assertEqual(str(Brand._meta.verbose_name_plural), "Brands")
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_string_representation(self):
        obj = Brand(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        translation.activate("en")
        self.assertEqual(Brand._meta.get_field("name").verbose_name, "name")
        self.assertEqual(Brand._meta.get_field("slug").verbose_name, "slug")
        self.assertEqual(Brand._meta.get_field("info").verbose_name, "info")
        self.assertEqual(Brand._meta.get_field("url").verbose_name, "url")
        self.assertEqual(Brand._meta.get_field("logo").verbose_name, "logo")
        self.assertEqual(Brand._meta.get_field("labels").verbose_name, "labels")
        self.assertEqual(
            Brand._meta.get_field("certificates").verbose_name, "certificates"
        )

        self.assertEqual(
            Brand._meta.get_field("date_created").verbose_name, "date created"
        )
        self.assertEqual(
            Brand._meta.get_field("date_updated").verbose_name, "date updated"
        )
        self.assertEqual(
            Brand._meta.get_field("last_updated_by").verbose_name, "last updated by"
        )
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_required_name_not_given_fails(self):
        pass

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = BrandFactory(name=name)
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        pass

    def test_logo_upload(self):
        pass

    def test_payment_options(self):
        pass


class SizeTest(TestCase):
    def test_verbose_name(self):
        translation.activate("en")
        self.assertEqual(str(Size._meta.verbose_name), "Size")
        self.assertEqual(str(Size._meta.verbose_name_plural), "Sizes")
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_string_representation(self):
        obj = Size(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        translation.activate("en")
        self.assertEqual(Size._meta.get_field("name").verbose_name, "name")
        self.assertEqual(Size._meta.get_field("slug").verbose_name, "slug")

        self.assertEqual(
            Size._meta.get_field("date_created").verbose_name, "date created"
        )
        self.assertEqual(
            Size._meta.get_field("date_updated").verbose_name, "date updated"
        )
        self.assertEqual(
            Size._meta.get_field("last_updated_by").verbose_name, "last updated by"
        )
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_required_name_not_given_fails(self):
        pass

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = SizeFactory(name=name)
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        pass


class ColorTest(TestCase):
    def test_verbose_name(self):
        translation.activate("en")
        self.assertEqual(str(Color._meta.verbose_name), "Color")
        self.assertEqual(str(Color._meta.verbose_name_plural), "Colors")
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_string_representation(self):
        obj = Color(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        translation.activate("en")
        self.assertEqual(Color._meta.get_field("name").verbose_name, "name")
        self.assertEqual(Color._meta.get_field("slug").verbose_name, "slug")

        self.assertEqual(
            Color._meta.get_field("date_created").verbose_name, "date created"
        )
        self.assertEqual(
            Color._meta.get_field("date_updated").verbose_name, "date updated"
        )
        self.assertEqual(
            Color._meta.get_field("last_updated_by").verbose_name, "last updated by"
        )
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_required_name_not_given_fails(self):
        pass

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = ColorFactory(name=name)
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        pass


class MaterialTest(TestCase):
    def test_verbose_name(self):
        translation.activate("en")
        self.assertEqual(str(Material._meta.verbose_name), "Material")
        self.assertEqual(str(Material._meta.verbose_name_plural), "Materials")
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_string_representation(self):
        obj = Material(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        translation.activate("en")
        self.assertEqual(Material._meta.get_field("name").verbose_name, "name")
        self.assertEqual(Material._meta.get_field("slug").verbose_name, "slug")
        self.assertEqual(Material._meta.get_field("info").verbose_name, "info")

        self.assertEqual(
            Material._meta.get_field("date_created").verbose_name, "date created"
        )
        self.assertEqual(
            Material._meta.get_field("date_updated").verbose_name, "date updated"
        )
        self.assertEqual(
            Material._meta.get_field("last_updated_by").verbose_name, "last updated by"
        )
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_required_name_not_given_fails(self):
        pass

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = MaterialFactory(name=name)
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        pass


class ProductTest(TestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        BrandFactory.create_batch(2)
        StoreFactory.create_batch(2)

    def test_verbose_name(self):
        # TODO: activate("nl"), then run checks for translated field names
        self.assertEqual(str(Product._meta.verbose_name), "Product")
        self.assertEqual(str(Product._meta.verbose_name_plural), "Products")

    def test_string_representation(self):
        obj = Product(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        translation.activate("en")
        self.assertEqual(Product._meta.get_field("name").verbose_name, "name")
        self.assertEqual(Product._meta.get_field("slug").verbose_name, "slug")
        self.assertEqual(Product._meta.get_field("info").verbose_name, "info")
        self.assertEqual(Product._meta.get_field("url").verbose_name, "url")
        self.assertEqual(
            Product._meta.get_field("cece_id").verbose_name, "cece product id"
        )
        self.assertEqual(Product._meta.get_field("price").verbose_name, "price")
        self.assertEqual(
            Product._meta.get_field("from_price").verbose_name, "from price"
        )
        self.assertEqual(
            Product._meta.get_field("main_image").verbose_name, "main image"
        )
        self.assertEqual(
            Product._meta.get_field("extra_images").verbose_name, "extra images"
        )
        self.assertEqual(Product._meta.get_field("brand").verbose_name, "brand")
        self.assertEqual(Product._meta.get_field("store").verbose_name, "store")
        self.assertEqual(
            Product._meta.get_field("categories").verbose_name, "categories"
        )
        self.assertEqual(
            Product._meta.get_field("subcategories").verbose_name, "subcategories"
        )
        self.assertEqual(Product._meta.get_field("materials").verbose_name, "materials")
        self.assertEqual(Product._meta.get_field("sizes").verbose_name, "sizes")
        self.assertEqual(Product._meta.get_field("colors").verbose_name, "colors")

        self.assertEqual(
            Product._meta.get_field("date_created").verbose_name, "date created"
        )
        self.assertEqual(
            Product._meta.get_field("date_updated").verbose_name, "date updated"
        )
        self.assertEqual(
            Product._meta.get_field("last_updated_by").verbose_name, "last updated by"
        )
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = ProductFactory(name=name)
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        pass

    def test_logo_upload(self):
        pass

    def test_payment_options(self):
        pass

    def test_product_brand_relation(self):
        pass

    def test_brand_addition(self):
        pass

    def test_brand_deletion(self):
        # CASCADE, so Product should be removed
        pass

    def test_product_store_relation(self):
        pass

    def test_store_addition(self):
        pass

    def test_store_deletion(self):
        # CASCADE, so Product should be removed
        pass

    def test_product_category_relation(self):
        pass

    def test_category_addition(self):
        pass

    def test_category_deletion(self):
        # TODO: What happens if the last Category is removed from Product?
        # We may not want to support Category-less Product instances
        pass

    def test_product_subcategory_relation(self):
        pass

    def test_subcategory_addition(self):
        pass

    def test_subcategory_deletion(self):
        pass

    def test_product_material_relation(self):
        pass

    def test_material_addition(self):
        pass

    def test_material_deletion(self):
        pass

    def test_product_color_relation(self):
        pass

    def test_color_addition(self):
        pass

    def test_color_deletion(self):
        pass

    def test_product_size_relation(self):
        pass

    def test_size_addition(self):
        pass

    def test_size_deletion(self):
        pass
