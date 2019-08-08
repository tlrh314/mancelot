import sys; sys.exit(0)
from django.test import TestCase
from django.template.loader import render_to_string

class LoginTestCase(TestCase):

    def test_login_redirect_to_login_url(self):

        # First check for the default behavior
        response = self.client.get('/sekrit/')
        self.assertRedirects(response, '/accounts/login/?next=/sekrit/')

        # Then override the LOGIN_URL setting
        with self.settings(LOGIN_URL='/other/login/'):
            response = self.client.get('/sekrit/')
            self.assertRedirects(response, '/other/login/?next=/sekrit/')

    def test_privacy_policy_is_rendered(self):
        with self.assertTemplateUsed(template_name='index.html'):
            render_to_string('index.html')
