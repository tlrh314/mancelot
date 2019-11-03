from django.test import TestCase
from django.template.loader import render_to_string


class AccountsViewsTestCase(TestCase):
    def test_index_is_rendered(self):
        with self.assertTemplateUsed(template_name="index.html"):
            render_to_string("index.html")

    def test_privacy_policy_is_rendered(self):
        with self.assertTemplateUsed(template_name="privacy_policy.html"):
            render_to_string("privacy_policy.html")
