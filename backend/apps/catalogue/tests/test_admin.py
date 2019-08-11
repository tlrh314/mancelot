from django.urls import reverse
from django.test import TestCase
from django.contrib.sites.models import Site

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
    ProductFactory
)
from accounts.factories import (
    UserModelFactory,
    AdminFactory,
)


class CatalogueAdminBaseTestCase(TestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.admin = AdminFactory(favorites__skip=True)
        self.admin.set_password("secret")
        self.admin.save()

        self.user = UserModelFactory(favorites__skip=True)
        self.user.set_password("secret")
        self.user.save()

        # Some defaults that are overwritten in the child class
        self.admin_changelist_uri = "admin:sites_site_changelist"
        self.admin_change_uri = "admin:sites_site_change"
        self.admin_change_pk = Site.objects.first().pk

    def tearDown(self, *args, **kwargs):
        self.admin.delete()
        self.user.delete()
        super().tearDown(*args, **kwargs)

    def test_login_of_admin_200(self):
        response = self.client.get(reverse("admin:login"))
        self.assertTemplateUsed(response, "admin/login.html")
        self.assertEqual(response.status_code, 200)
        login_status = self.client.login(email=self.admin.email, password="secret")
        self.assertTrue(login_status)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)

    def test_login_of_user_302(self):
        response = self.client.get(reverse("admin:login"))
        self.assertTemplateUsed(response, "admin/login.html")
        self.assertEqual(response.status_code, 200)  # login form is fine
        login_status = self.client.login(email=self.user.email, password="secret")
        self.assertTrue(login_status)  # b/c admin login forms works for any user

        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)  # the index is not fine
        self.assertEqual(response.url, "/admin/login/?next=/admin/")

    def test_get_admin_changelist_is_superuser_200(self):
        self.client.login(email=self.admin.email, password="secret")
        response = self.client.get(reverse(self.admin_changelist_uri))
        self.assertEqual(response.status_code, 200)

    def test_get_admin_changelist_is_authenticated_302(self):
        self.client.login(email=self.user.email, password="secret")
        uri = reverse(self.admin_changelist_uri)
        response = self.client.get(uri)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/admin/login/?next="+uri)

    def test_get_admin_change_is_superuser_200(self):
        self.client.login(email=self.admin.email, password="secret")
        uri = reverse(self.admin_change_uri, args=[self.admin_change_pk])
        response = self.client.get(uri)
        self.assertEqual(response.status_code, 200)

    def test_get_admin_change_is_authenticated_302(self):
        self.client.login(email=self.user.email, password="secret")
        uri = reverse(self.admin_change_uri, args=[self.admin_change_pk])
        response = self.client.get(uri)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/admin/login/?next="+uri)

    def test_admin_detail_view_can_be_saved(self):
        pass

    def test_admin_save_updates_last_updated_by(self):
        pass


class RelatedDropdownFilterTest(TestCase):
    def test_something(self):
        pass


class CeceLabelAdminTest(CatalogueAdminBaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        if CeceLabel.objects.count() < 5:
            CeceLabelFactory.create_batch(5 - CeceLabel.objects.count())

    def setUp(self):
        # Set the admin + session
        super().setUp()

        # Set the detail for this specific test
        self.admin_changelist_uri = "admin:catalogue_cecelabel_changelist"
        self.admin_change_uri = "admin:catalogue_cecelabel_change"
        self.admin_change_pk = CeceLabel.objects.last().pk
        self.count = CeceLabel.objects.count()
        # TODO: sanity check that the uri is resolved correctly
        self.resource_name_list = "CeceLabel List"
        self.resource_name_detail = "CeceLabel Instance"


class CertificateAdminTest(CatalogueAdminBaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        if Certificate.objects.count() < 20:
            CertificateFactory.create_batch(20 - Certificate.objects.count())

    def setUp(self):
        # Set the admin + session
        super().setUp()

        # Set the detail for this specific test
        self.admin_changelist_uri = "admin:catalogue_certificate_changelist"
        self.admin_change_uri = "admin:catalogue_certificate_change"
        self.admin_change_pk = Certificate.objects.last().pk
        self.count = Certificate.objects.count()


class SubcategoryAdminInline(TestCase):
    def test_something(self):
        pass


class CategoryAdminTest(CatalogueAdminBaseTestCase):

    @classmethod
    def setUpTestData(cls):
        if Category.objects.count() < 20:
            CategoryFactory.create_batch(20 - Category.objects.count(),
                # subcategories__skip=True
            )
    def setUp(self):
        # Set the admin + session
        super().setUp()

        # Set the detail for this specific test
        self.admin_changelist_uri = "admin:catalogue_category_changelist"
        self.admin_change_uri = "admin:catalogue_category_change"
        self.admin_change_pk = Category.objects.last().pk
        self.count = Category.objects.count()


class PaymentOptionAdminTest(CatalogueAdminBaseTestCase):
    def setUp(self):
        # Set the admin + session
        super().setUp()

        if PaymentOption.objects.count() < 20:
            PaymentOptionFactory.create_batch(20 - PaymentOption.objects.count())

        # Set the detail for this specific test
        self.admin_changelist_uri = "admin:catalogue_paymentoption_changelist"
        self.admin_change_uri = "admin:catalogue_paymentoption_change"
        self.admin_change_pk = PaymentOption.objects.last().pk
        self.count = PaymentOption.objects.count()


class StoreAdminTest(CatalogueAdminBaseTestCase):
    @classmethod
    def setUpTestData(cls):
        if Store.objects.count() < 40:
            StoreFactory.create_batch(40 - Store.objects.count())

    def setUp(self):
        # Set the admin + session
        super().setUp()

        # Set the detail for this specific test
        self.admin_changelist_uri = "admin:catalogue_store_changelist"
        self.admin_change_uri = "admin:catalogue_store_change"
        self.admin_change_pk = Store.objects.last().pk
        self.count = Store.objects.count()


class BrandAdminTest(CatalogueAdminBaseTestCase):
    @classmethod
    def setUpTestData(cls):
        if Brand.objects.count() < 100:
            BrandFactory.create_batch(100 - Brand.objects.count())

    def setUp(self):
        # Set the admin + session
        super().setUp()

        # Set the detail for this specific test
        self.admin_changelist_uri = "admin:catalogue_brand_changelist"
        self.admin_change_uri = "admin:catalogue_brand_change"
        self.admin_change_pk = Brand.objects.last().pk
        self.count = Brand.objects.count()


class SizeAdminTest(CatalogueAdminBaseTestCase):
    @classmethod
    def setUpTestData(cls):
        if Size.objects.count() < 50:
            SizeFactory.create_batch(50 - Size.objects.count())

    def setUp(self):
        # Set the admin + session
        super().setUp()

        # Set the detail for this specific test
        self.admin_changelist_uri = "admin:catalogue_size_changelist"
        self.admin_change_uri = "admin:catalogue_size_change"
        self.admin_change_pk = Size.objects.last().pk
        self.count = Size.objects.count()


class MaterialAdminTest(CatalogueAdminBaseTestCase):
    @classmethod
    def setUpTestData(cls):
        if Material.objects.count() < 50:
            MaterialFactory.create_batch(50 - Material.objects.count())

    def setUp(self):
        # Set the admin + session
        super().setUp()

        # Set the detail for this specific test
        self.admin_changelist_uri = "admin:catalogue_material_changelist"
        self.admin_change_uri = "admin:catalogue_material_change"
        self.admin_change_pk = Material.objects.last().pk
        self.count = Material.objects.count()


class ProductAdminTest(CatalogueAdminBaseTestCase):
    @classmethod
    def setUpTestData(self):
        if Store.objects.count() < 5:
            StoreFactory.create_batch(5 - Store.objects.count())
        if Brand.objects.count() < 10:
            BrandFactory.create_batch(10 - Brand.objects.count())
        if Product.objects.count() < 50:
            ProductFactory.create_batch(50 - Product.objects.count())

    def setUp(self):
        # Set the admin + session
        super().setUp()

        # Set the detail for this specific test
        self.admin_changelist_uri = "admin:catalogue_product_changelist"
        self.admin_change_uri = "admin:catalogue_product_change"
        self.admin_change_pk = Product.objects.last().pk
        self.count = Product.objects.count()

    def test_list_display(self):
        pass

    def test_list_filter(self):
        pass

    def test_list_filters_give_correct_querysets(self):
        pass

    def test_search_fields(self):
        pass

    def test_ordering(self):
        pass

    def test_filter_horizontal(self):
        pass

    def test_form_override_with_fix_tinymce_has_too_wide_ui_form(self):
        pass

    def test_fieldsets(self):
        pass

    def test_set_section_through_category(self):
        pass

    def test_set_first_category_through_category(self):
        pass

    def test_history_view_renders_html(self):
        pass

    def test_product_is_on_sale_filter_gives_correct_querysets(self):
        pass
