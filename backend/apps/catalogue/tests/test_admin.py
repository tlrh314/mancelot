from django.urls import reverse
from django.test import TestCase

from catalogue.admin import (
    RelatedDropdownFilter,
    CeceLabelAdmin,
    CertificateAdmin,
    SubcategoryAdminInline,
    CategoryAdmin,
    PaymentOption,
    StoreAdmin,
    BrandAdmin,
    SizeAdmin,
    MaterialAdmin,
    ProductIsOnSaleFilter,
    ProductAdmin
)
from accounts.factories import AdminFactory


class CatalogueAdminBaseTestCase(TestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.admin = AdminFactory(favorites__skip=True)
        self.admin.set_password("secret")
        self.admin.save()

    def test_login(self):
        response = self.client.get(reverse("admin:login"))
        self.assertTemplateUsed(response, "admin/login.html")
        self.assertEqual(response.status_code, 200)
        login_status = self.client.login(email=self.admin.email, password="secret")
        self.assertTrue(login_status)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)

    def tearDown(self, *args, **kwargs):
        self.admin.delete()
        super().tearDown(*args, **kwargs)


class RelatedDropdownFilterTest(CatalogueAdminBaseTestCase):
    def test_something(self):
        raise NotImplementedError


class CeceLabelAdminTest(CatalogueAdminBaseTestCase):
    def test_admin_list_view_can_be_opened(self):
        raise NotImplementedError
        reverse("admin:catalogue_cecelabel_changelist")

    def test_admin_detail_view_can_be_opened(self):
        raise NotImplementedError
        reverse("admin:catalogue_cecelabel_change", args=[])

    def test_admin_detail_view_can_be_saved(self):
        raise NotImplementedError

    def test_admin_save_updates_last_updated_by(self):
        raise NotImplementedError


class CertificateAdminTest(CatalogueAdminBaseTestCase):
    def test_admin_list_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_saved(self):
        raise NotImplementedError

    def test_admin_save_updates_last_updated_by(self):
        raise NotImplementedError


class SubcategoryAdminInline(CatalogueAdminBaseTestCase):
    def test_something(self):
        raise NotImplementedError


class CategoryAdminTest(CatalogueAdminBaseTestCase):
    def test_admin_list_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_saved(self):
        raise NotImplementedError

    def test_admin_save_updates_last_updated_by(self):
        raise NotImplementedError


class PaymentOptionTest(CatalogueAdminBaseTestCase):
    def test_admin_list_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_saved(self):
        raise NotImplementedError

    def test_admin_save_updates_last_updated_by(self):
        raise NotImplementedError


class StoreAdminTest(CatalogueAdminBaseTestCase):
    def test_admin_list_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_saved(self):
        raise NotImplementedError

    def test_admin_save_updates_last_updated_by(self):
        raise NotImplementedError


class BrandAdminTest(CatalogueAdminBaseTestCase):
    def test_admin_list_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_saved(self):
        raise NotImplementedError

    def test_admin_save_updates_last_updated_by(self):
        raise NotImplementedError


class SizeAdminTest(CatalogueAdminBaseTestCase):
    def test_admin_list_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_saved(self):
        raise NotImplementedError

    def test_admin_save_updates_last_updated_by(self):
        raise NotImplementedError


class MaterialAdminTest(CatalogueAdminBaseTestCase):
    def test_admin_list_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_saved(self):
        raise NotImplementedError

    def test_admin_save_updates_last_updated_by(self):
        raise NotImplementedError


class ProductAdminTest(CatalogueAdminBaseTestCase):
    def test_admin_list_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_opened(self):
        raise NotImplementedError

    def test_admin_detail_view_can_be_saved(self):
        raise NotImplementedError

    def test_admin_save_updates_last_updated_by(self):
        raise NotImplementedError

    def test_list_display(self):
        raise NotImplementedError

    def test_list_filter(self):
        raise NotImplementedError

    def test_list_filters_give_correct_querysets(self):
        raise NotImplementedError

    def test_search_fields(self):
        raise NotImplementedError

    def test_ordering(self):
        raise NotImplementedError

    def test_filter_horizontal(self):
        raise NotImplementedError

    def test_form_override_with_fix_tinymce_has_too_wide_ui_form(self):
        raise NotImplementedError

    def test_fieldsets(self):
        raise NotImplementedError

    def test_set_section_through_category(self):
        raise NotImplementedError

    def test_set_first_category_through_category(self):
        raise NotImplementedError

    def test_history_view_renders_html(self):
        raise NotImplementedError

    def test_product_is_on_sale_filter_gives_correct_querysets(self):
        raise NotImplementedError
