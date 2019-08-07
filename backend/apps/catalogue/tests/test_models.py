from faker import Faker
from django.test import TestCase
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
    Material,
    Product
)


faker = Faker()


class CeceLabelTest(TestCase):
    def test_verbose_name(self):
        self.assertEqual(str(CeceLabel._meta.verbose_name), "Label")
        self.assertEqual(str(CeceLabel._meta.verbose_name_plural), "Labels")

    def test_string_representation(self):
        obj = CeceLabel(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        obj = CeceLabel()
        name = "naam"
        slug = "slug"
        info = "info"
        cece_api_url = "cece_api_url"
        raise NotImplementedError

    def test_required_name_not_given_fails(self):
        raise NotImplementedError
        # self.assertRaises(FooException, Thing, name="1234")
        with self.assertRaisesMessage(ValueError, "invalid literal for int()"):
            obj = CeceLabel(
                info=faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
            )
            obj.save()

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = CeceLabel(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError


class CertificateTest(TestCase):
    def test_verbose_name(self):
        self.assertEqual(str(Certificate._meta.verbose_name), "Certificaat")
        self.assertEqual(str(Certificate._meta.verbose_name_plural), "Certificaten")

    def test_string_representation(self):
        obj = Certificate(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        obj = Certificate()
        name = "naam"
        slug = "slug"
        info = "info"
        cece_api_url = "cece_api_url"
        raise NotImplementedError

    def test_required_name_not_given_fails(self):
        raise NotImplementedError
        obj = Certificate(
            info=faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
        )
        obj.save()

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = Certificate(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError


class CategoryTest(TestCase):
    def test_verbose_name(self):
        self.assertEqual(str(Category._meta.verbose_name), "Categorie")
        self.assertEqual(str(Category._meta.verbose_name_plural), "Categorieën")

    def test_string_representation(self):
        obj = Category(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        obj = Category()
        name = "naam"
        slug = "slug"
        section = "sectie"
        raise NotImplementedError

    def test_required_name_not_given_fails(self):
        raise NotImplementedError
        obj = Category(
            info=faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
        )
        obj.save()

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = Category(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError

    def test_default_section(self):
        obj = Category()
        self.assertEqual(obj.section, 0)

    def test_category_subcategory_creation(self):
        category = Category(name="Ondergoed & Sokken")
        subcategory1 = Subcategory(name="Ondergoed", category=category)
        subcategory2 = Subcategory(name="Sokken", category=category)

        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Subcategory.objects.count(), 2)
        self.assertEqual(Subcategory.objects.count(), 2)
        self.assertEqual(category.subcategories.all(), 2)
        self.assertEqual(category.subcategories.first(), subcategory1)
        self.assertEqual(category.subcategories.last(), subcategory2)
        self.assertEqual(subcategory1.category, category)
        self.assertEqual(subcategory2.category, category)

    def test_delete_cascades_down_to_foreign_key_subcategory_deletion(self):
        category = Category(name="Ondergoed & Sokken")
        subcategory1 = Subcategory(name="Ondergoed", category=category)
        subcategory2 = Subcategory(name="Sokken", category=category)

        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Subcategory.objects.count(), 2)
        self.assertEqual(Subcategory.objects.count(), 2)

        # Now delete
        category.delete()
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(Subcategory.objects.count(), 0)
        self.assertEqual(Subcategory.objects.count(), 0)


class SubcategoryTest(TestCase):
    def test_verbose_name(self):
        self.assertEqual(str(Subcategory._meta.verbose_name), "Categorie")
        self.assertEqual(str(Subcategory._meta.verbose_name_plural), "Categorieën")

    def test_string_representation(self):
        obj = Subcategory(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        raise NotImplementedError
        obj = Subcategory()
        name = "naam"
        slug = "slug"

    def test_required_name_not_given_fails(self):
        raise NotImplementedError
        obj = Subcategory(
            info=faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
        )
        obj.save()

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        category = Category(name="Category")
        obj = Subcategory(category=category, name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError


class PaymentOptionTest(TestCase):
    def test_verbose_name(self):
        self.assertEqual(str(PaymentOption._meta.verbose_name), "Betaalmethode")
        self.assertEqual(str(PaymentOption._meta.verbose_name_plural), "Betaalmethodes")

    def test_string_representation(self):
        obj = PaymentOption(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        raise NotImplementedError
        obj = PaymentOption()
        name = "naam"
        slug = "slug"
        info = "info"

    def test_required_name_not_given_fails(self):
        raise NotImplementedError
        # self.assertRaises(FooException, Thing, name="1234")
        with self.assertRaisesMessage(ValueError, "invalid literal for int()"):
            obj = PaymentOption(
                info=faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
            )
            obj.save()

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = PaymentOption(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))

    def test_absolute_url(self):
        pass

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError

    def test_logo_upload(self):
        raise NotImplementedError


class StoreTest(TestCase):
    def setUp(self):
        pass

    def test_verbose_name(self):
        self.assertEqual(str(Store._meta.verbose_name), "Winkel")
        self.assertEqual(str(Store._meta.verbose_name_plural), "Winkels")

    def test_string_representation(self):
        obj = Store(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        raise NotImplementedError
        obj = Store()
        name = "naam"
        slug = "slug"
        info = "info"
        url = "url"
        logo = "logo"

    def test_required_name_not_given_fails(self):
        raise NotImplementedError
        # self.assertRaises(FooException, Thing, name="1234")
        with self.assertRaisesMessage(ValueError, "invalid literal for int()"):
            obj = Store(
                info=faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
            )
            obj.save()

    def test_slug_creation_on_save(self):
        raise NotImplementedError
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = Store(name=name)  # factory
        obj.save()
        self.assertEqual(obj.slug, slugify(name))

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError

    def test_logo_upload(self):
        raise NotImplementedError

    def test_payment_options(self):
        raise NotImplementedError


class BrandTest(TestCase):
    def setUp(self):
        pass

    def test_verbose_name(self):
        self.assertEqual(str(Brand._meta.verbose_name), "Merk")
        self.assertEqual(str(Brand._meta.verbose_name_plural), "Merken")

    def test_string_representation(self):
        obj = Brand(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        raise NotImplementedError
        obj = Brand()
        name = "naam"
        slug = "slug"
        info = "info"
        url = "url"
        logo = "logo"

    def test_required_name_not_given_fails(self):
        # self.assertRaises(FooException, Thing, name="1234")
        with self.assertRaisesMessage(ValueError, "invalid literal for int()"):
            obj = Brand(
                info=faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
            )
            obj.save()

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = Brand(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError

    def test_logo_upload(self):
        raise NotImplementedError

    def test_payment_options(self):
        raise NotImplementedError


class SizeTest(TestCase):
    def test_verbose_name(self):
        self.assertEqual(str(Size._meta.verbose_name), "Maat")
        self.assertEqual(str(Size._meta.verbose_name_plural), "Maten")

    def test_string_representation(self):
        obj = Size(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        raise NotImplementedError
        obj = Size()
        name = "naam"
        slug = "slug"

    def test_required_name_not_given_fails(self):
        raise NotImplementedError

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = Size(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError


class MaterialTest(TestCase):
    def test_verbose_name(self):
        self.assertEqual(str(Material._meta.verbose_name), "Materiaal")
        self.assertEqual(str(Material._meta.verbose_name_plural), "Materialen")

    def test_string_representation(self):
        obj = Material(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        raise NotImplementedError
        obj = Material()
        name = "naam"
        slug = "slug"
        info = "info"

    def test_required_name_not_given_fails(self):
        raise NotImplementedError

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = Material(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError


class ProductTest(TestCase):
    def setUp(self):
        pass

    def test_verbose_name(self):
        self.assertEqual(str(Product._meta.verbose_name), "Product")
        self.assertEqual(str(Product._meta.verbose_name_plural), "Producten")

    def test_string_representation(self):
        obj = Product(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        raise NotImplementedError
        obj = Product()
        name = "naam"
        slug = "slug"
        info = "info"
        url = "url"
        logo = "logo"
        main_image = "hoofdafbeelding"
        extra_images = "extra afbeeldingen"
        # brand, store, category, subcategory, material, size
        color = "kleur"

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = Product(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError

    def test_logo_upload(self):
        raise NotImplementedError

    def test_payment_options(self):
        raise NotImplementedError

    def test_product_brand_relation(self):
        raise NotImplementedError

    def test_brand_deletion(self):
        # CASCADE, so Product should be removed
        raise NotImplementedError

    def test_product_store_relation(self):
        raise NotImplementedError

    def test_store_deletion(self):
        # CASCADE, so Product should be removed
        raise NotImplementedError

    def test_product_category_relation(self):
        raise NotImplementedError

    def test_category_deletion(self):
        # What happens if the last Category is removed from Product?
        # We may not want to support Category-less Product instances
        raise NotImplementedError

    def test_product_subcategory_relation(self):
        raise NotImplementedError

    def test_subcategory_deletion(self):
        raise NotImplementedError

    def test_product_material_relation(self):
        raise NotImplementedError

    def test_material_deletion(self):
        raise NotImplementedError

    def test_product_size_relation(self):
        raise NotImplementedError

    def test_size_deletion(self):
        raise NotImplementedError
