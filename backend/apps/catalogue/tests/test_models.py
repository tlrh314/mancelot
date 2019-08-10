from faker import Faker
from django.test import TestCase
from django.utils.text import slugify
from django.core.exceptions import ValidationError


faker = Faker()


class CeceLabelTest(TestCase):
    def test_verbose_name(self):
        # TODO: activate("nl"), then run checks for translated field names
        self.assertEqual(str(CeceLabel._meta.verbose_name), "Label")
        self.assertEqual(str(CeceLabel._meta.verbose_name_plural), "Labels")

    def test_string_representation(self):
        obj = CeceLabel(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        # TODO: activate("nl"), then run checks for translated field names
        obj = CeceLabelFactory.build()
        name = "name"
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
        obj = CeceLabelFactory(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError


class CertificateTest(TestCase):
    def test_verbose_name(self):
        # TODO: activate("nl"), then run checks for translated field names
        self.assertEqual(str(Certificate._meta.verbose_name), "Certificate")
        self.assertEqual(str(Certificate._meta.verbose_name_plural), "Certificates")

    def test_string_representation(self):
        obj = Certificate(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        # TODO: activate("nl"), then run checks for translated field names
        obj = CertificateFactory.build()
        name = "name"
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
        obj = CertificateFactory(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError


class CategoryTest(TestCase):
    def test_verbose_name(self):
        # TODO: activate("nl"), then run checks for translated field names
        self.assertEqual(str(Category._meta.verbose_name), "Category")
        self.assertEqual(str(Category._meta.verbose_name_plural), "Categories")

    def test_string_representation(self):
        obj = Category(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        # TODO: activate("nl"), then run checks for translated field names
        obj = CategoryFactory.build()
        name = "name"
        slug = "slug"
        section = "section"
        raise NotImplementedError

    def test_required_name_not_given_fails(self):
        raise NotImplementedError
        obj = Category(
            info=faker.text(max_nb_chars=faker.random_int(min=42, max=1337))
        )
        obj.save()

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = CategoryFactory(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

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
        # TODO: activate("nl"), then run checks for translated field names
        self.assertEqual(str(Subcategory._meta.verbose_name), "Categorie")
        self.assertEqual(str(Subcategory._meta.verbose_name_plural), "Categorieën")

    def test_string_representation(self):
        obj = Subcategory(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        # TODO: activate("nl"), then run checks for translated field names
        raise NotImplementedError
        obj = SubcategoryFactory.build()
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
        category = SubcategoryFactory(name="Category")
        obj.save()
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_absolute_url(self):
        return

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError


class PaymentOptionTest(TestCase):
    def test_verbose_name(self):
        # TODO: activate("nl"), then run checks for translated field names
        self.assertEqual(str(PaymentOption._meta.verbose_name), "Betaalmethode")
        self.assertEqual(str(PaymentOption._meta.verbose_name_plural), "Betaalmethodes")

    def test_string_representation(self):
        obj = PaymentOption(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        # TODO: activate("nl"), then run checks for translated field names
        raise NotImplementedError
        obj = PaymentOptionFactory.build()
        name = "name"
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
        obj.delete()

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
        # TODO: activate("nl"), then run checks for translated field names
        self.assertEqual(str(Store._meta.verbose_name), "Store")
        self.assertEqual(str(Store._meta.verbose_name_plural), "Stores")

    def test_string_representation(self):
        obj = Store(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        # TODO: activate("nl"), then run checks for translated field names
        raise NotImplementedError
        obj = StoreFactory.build()
        name = "name"
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
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = StoreFactory(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

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
        # TODO: activate("nl"), then run checks for translated field names
        self.assertEqual(str(Brand._meta.verbose_name), "Brand")
        self.assertEqual(str(Brand._meta.verbose_name_plural), "Brands")

    def test_string_representation(self):
        obj = Brand(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        # TODO: activate("nl"), then run checks for translated field names
        raise NotImplementedError
        obj = BrandFactory.build()
        name = "name"
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
        obj = BrandFactory(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

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
        # TODO: activate("nl"), then run checks for translated field names
        self.assertEqual(str(Size._meta.verbose_name), "Size")
        self.assertEqual(str(Size._meta.verbose_name_plural), "Sizes")

    def test_string_representation(self):
        obj = Size(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        # TODO: activate("nl"), then run checks for translated field names
        raise NotImplementedError
        obj = SizeFactory.build()
        name = "name"
        slug = "slug"

    def test_required_name_not_given_fails(self):
        raise NotImplementedError

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = SizeFactory(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError


class ColorTest(TestCase):
    def test_verbose_name(self):
        # TODO: activate("nl"), then run checks for translated field names
        self.assertEqual(str(Color._meta.verbose_name), "Color")
        self.assertEqual(str(Color._meta.verbose_name_plural), "Colors")

    def test_string_representation(self):
        obj = Color(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        # TODO: activate("nl"), then run checks for translated field names
        raise NotImplementedError
        obj = ColorFactory.build()
        name = "name"
        slug = "slug"

    def test_required_name_not_given_fails(self):
        raise NotImplementedError

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = ColorFactory(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError


class MaterialTest(TestCase):
    def test_verbose_name(self):
        # TODO: activate("nl"), then run checks for translated field names
        self.assertEqual(str(Material._meta.verbose_name), "Material")
        self.assertEqual(str(Material._meta.verbose_name_plural), "Materials")

    def test_string_representation(self):
        obj = Material(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        # TODO: activate("nl"), then run checks for translated field names
        raise NotImplementedError
        obj = MaterialFactory.build()
        name = "name"
        slug = "slug"
        info = "info"

    def test_required_name_not_given_fails(self):
        raise NotImplementedError

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = MaterialFactory(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

    def test_deletion_of_last_updated_by_user(self):
        # SET_NULL
        raise NotImplementedError


class ProductTest(TestCase):
    def setUp(self):
        pass

    def test_verbose_name(self):
        # TODO: activate("nl"), then run checks for translated field names
        self.assertEqual(str(Product._meta.verbose_name), "Product")
        self.assertEqual(str(Product._meta.verbose_name_plural), "Products")

    def test_string_representation(self):
        obj = Product(name="name")
        self.assertEqual(str(obj), "{0}".format(obj.name))

    def test_field_names(self):
        # TODO: activate("nl"), then run checks for translated field names
        raise NotImplementedError
        obj = ProductFactory.build()
        name = "name"
        slug = "slug"
        info = "info"
        url = "url"
        logo = "logo"
        main_image = "main image"
        extra_images = "extra images"
        # TODO: add translations to fk/m2m model fields
        # brand, store, categories, subcategories, materials, sizes
        color = "color"

    def test_slug_creation_on_save(self):
        name = "(*$jdskfasdf yhjkF~di `qo` oasu*OYUGHJKAf"
        obj = ProductFactory(name=name)
        obj.save()
        self.assertEqual(obj.slug, slugify(name))
        obj.delete()

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

    def test_brand_addition(self):
        raise NotImplementedError

    def test_brand_deletion(self):
        # CASCADE, so Product should be removed
        raise NotImplementedError

    def test_product_store_relation(self):
        raise NotImplementedError

    def test_store_addition(self):
        raise NotImplementedError

    def test_store_deletion(self):
        # CASCADE, so Product should be removed
        raise NotImplementedError

    def test_product_category_relation(self):
        raise NotImplementedError

    def test_category_addition(self):
        raise NotImplementedError

    def test_category_deletion(self):
        # What happens if the last Category is removed from Product?
        # We may not want to support Category-less Product instances
        raise NotImplementedError

    def test_product_subcategory_relation(self):
        raise NotImplementedError

    def test_subcategory_addition(self):
        raise NotImplementedError

    def test_subcategory_deletion(self):
        raise NotImplementedError

    def test_product_material_relation(self):
        raise NotImplementedError

    def test_material_addition(self):
        raise NotImplementedError

    def test_material_deletion(self):
        raise NotImplementedError

    def test_product_color_relation(self):
        raise NotImplementedError

    def test_color_addition(self):
        raise NotImplementedError

    def test_color_deletion(self):
        raise NotImplementedError

    def test_product_size_relation(self):
        raise NotImplementedError

    def test_size_addition(self):
        raise NotImplementedError

    def test_size_deletion(self):
        raise NotImplementedError
