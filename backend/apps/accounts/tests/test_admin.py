from django.test import TestCase

from accounts.admin import UserModelAdmin


class ProductAdminTest(TestCase):
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

    def test_send_password_reset_action(self):
        raise NotImplementedError

    def test_add_fieldsets_override(self):
        raise NotImplementedError

    def test_adding_user_instance(self):
        raise NotImplementedError

    def test_change_user_password(self):
        raise NotImplementedError

    def test_fieldsets(self):
        raise NotImplementedError

    def test_history_view_renders_html(self):
        raise NotImplementedError
