from django.test import TestCase

from accounts.models import UserModel
from catalogue.tests.test_admin import CatalogueAdminBaseTestCase


class UserModelAdminTestCase(CatalogueAdminBaseTestCase, TestCase):
    def setUp(self, *args, **kwargs):
        # Set the admin + session
        super().setUp(*args, **kwargs)

        # Set the detail for this specific test
        self.admin_changelist_uri = "admin:accounts_usermodel_changelist"
        self.admin_add_uri = "admin:accounts_usermodel_add"
        self.admin_change_uri = "admin:accounts_usermodel_change"
        self.admin_delete_uri = "admin:accounts_usermodel_delete"
        self.admin_history_uri = "admin:accounts_usermodel_history"
        self.admin_instance_pk = UserModel.objects.last().pk
        self.count = UserModel.objects.count()

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

    def test_send_password_reset_action(self):
        pass

    def test_add_fieldsets_override(self):
        pass

    def test_adding_user_instance(self):
        pass

    def test_change_user_password(self):
        pass

    def test_fieldsets(self):
        pass

    def test_history_view_renders_html(self):
        pass
