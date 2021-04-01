from django.test import TestCase
from django.contrib.auth import get_user_model

from catalogue.models import Brand
from catalogue.models import Store
from catalogue.models import Product
from catalogue.models import Category
from catalogue.models import Subcategory
from catalogue.models import Certificate


# self.assertIsNotNone(entry.get_absolute_url())


# RequestFactory
# class IndexTests(TestCase):
#
#     def setUp(self):
#         self.user = get_user_model().objects.create(
#             email="timo@mancelot.nl", full_name="Timo Halbesma"
#         )
#
#     def test_one_entry(self):
#         Entry.objects.create(title='1-title', body='1-body', author=self.user)
#         response = self.client.get('/')
#         self.assertContains(response, '1-title')
#         self.assertContains(response, '1-body')
#
#     def test_two_entries(self):
#         Entry.objects.create(title='1-title', body='1-body', author=self.user)
#         Entry.objects.create(title='2-title', body='2-body', author=self.user)
#         response = self.client.get('/')
#         self.assertContains(response, '1-title')
#         self.assertContains(response, '1-body')
#         self.assertContains(response, '2-title')

#     def test_title_in_entry(self):
#         response = self.client.get(self.entry.get_absolute_url())
#         self.assertContains(response, self.entry.title)
#
#     def test_body_in_entry(self):
#         response = self.client.get(self.entry.get_absolute_url())
#         self.assertContains(response, self.entry.body)
