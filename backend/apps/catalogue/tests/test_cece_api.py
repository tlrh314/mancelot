import json
import requests
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.factories import AdminFactory
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
    Product
)


def response_to_json(response):
    return json.loads(response.content.decode("utf8"))


class CeceRemoteAPIBaseTestCase(APITestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)  # in case of inheritance

        # Obtain JSON Web Token for a superuser
        self.ceceuser = AdminFactory(email=settings.CECE_API_USER, favorites__skip=True)
        self.ceceuser.set_password(settings.CECE_API_PASS)
        self.ceceuser.save()
        response = requests.post(
            "{0}v1/token/".format(settings.CECE_API_URI), {
                "email": self.ceceuser.email, "password": settings.CECE_API_PASS,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response_to_json(response)
        self.headers = {
            "Authorization": "Bearer {0}".format(data["access"]),
            "Accept": "application/json",
            "user-agent": "Mancelot Bot v1.3.3.7"
        }

        # Defaults, overwritten in child classes
        self.resource_uri = settings.CECE_API_URI + "mancelot/catalog/paymethod/"
        self.expected_fields = [
            "id", "name", "icon_url"
        ]

    def tearDown(self, *args, **kwargs):
        self.ceceuser.delete()
        super().tearDown(*args, **kwargs)

    def test_get_cece_api_200_and_check_data(self):
        response = requests.get(self.resource_uri, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response_to_json(response)
        self.assertIn("count", data.keys())
        self.assertIn("next", data.keys())
        self.assertIn("previous", data.keys())
        self.assertIn("results", data.keys())
        first = data["results"][0]
        for field in self.expected_fields:
            self.assertIn(field, first.keys())

        detail_uri = "{0}{1}/".format(self.resource_uri, first["id"])
        response = requests.get(detail_uri, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response_to_json(response)
        for field in self.expected_fields:
            self.assertIn(field, data.keys())


class CeceRemoteAPIPayMethodTestCase(CeceRemoteAPIBaseTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.resource_uri = settings.CECE_API_URI + "mancelot/catalog/paymethod/"
        self.expected_fields = [
            "id", "name", "icon_url",
        ]


class CeceRemoteAPILabelTestCase(CeceRemoteAPIBaseTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.resource_uri = settings.CECE_API_URI + "mancelot/catalog/label/"
        self.expected_fields = [
            "id", "abbreviation", "label_name", "description"
        ]


class CeceRemoteAPICertificateTestCase(CeceRemoteAPIBaseTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.resource_uri = settings.CECE_API_URI + "mancelot/catalog/certificate/"
        self.expected_fields = [
            "id", "name", "short_description", "about", "static_url"
        ]


class CeceRemoteAPICategoryTestCase(CeceRemoteAPIBaseTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.resource_uri = settings.CECE_API_URI + "mancelot/catalog/category/"
        self.expected_fields = [
            "id", "category_name", "category_ID", "type", "subcategory"
        ]


class CeceRemoteAPIStoreTestCase(CeceRemoteAPIBaseTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.resource_uri = settings.CECE_API_URI + "mancelot/catalog/store/"
        self.expected_fields = [
            "id", "store_name", "about", "store_url", "logo", "pay_methods",
        ]


class CeceRemoteAPIBrandTestCase(CeceRemoteAPIBaseTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.resource_uri = settings.CECE_API_URI + "mancelot/catalog/brand/"
        self.expected_fields = [
            "id", "brand_name", "about_brand", "labels", "certificate", "about_brand",
        ]


class CeceRemoteAPIProductTestCase(CeceRemoteAPIBaseTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.resource_uri = settings.CECE_API_URI + "mancelot/catalog/product/"
        self.expected_fields = [
            "id", "title", "text", "extra_text", "link",
            "productID", "price", "old_price",
            "primary_image", "extra_images",
            "color", "sizes", "size", "material",
            "category", "subcategory",
            "brand", "store",
        ]
