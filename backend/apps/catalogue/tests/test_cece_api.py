import json
import requests
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.factories import AdminFactory
from catalogue.utils import response_to_json
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


class CeceRemoteAPIBaseTestCase(object):
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


class CeceRemoteAPIPayMethodTestCase(CeceRemoteAPIBaseTestCase, APITestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.resource_uri = settings.CECE_API_URI + "mancelot/catalog/paymethod/"
        self.expected_fields = [
            "id", "name", "icon_url",
        ]

    def test_create_instance_with_cece_data(self):
        response = requests.get(self.resource_uri, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response_to_json(response)
        self.assertGreater(data["count"], 0)

        external_obj = data["results"][0]
        obj = PaymentOption.objects.create(
            name=external_obj["name"],
            logo=external_obj["icon_url"],
            cece_api_url="{0}{1}/".format(self.resource_uri, external_obj["id"]),
            last_updated_by=self.ceceuser,
        )
        self.assertEqual(PaymentOption.objects.filter(pk=obj.pk).exists(), True)


class CeceRemoteAPILabelTestCase(CeceRemoteAPIBaseTestCase, APITestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.resource_uri = settings.CECE_API_URI + "mancelot/catalog/label/"
        self.expected_fields = [
            "id", "abbreviation", "label_name", "description"
        ]

    def test_create_instance_with_cece_data(self):
        response = requests.get(self.resource_uri, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response_to_json(response)
        self.assertGreater(data["count"], 0)

        external_obj = data["results"][0]
        obj = CeceLabel.objects.create(
            name=external_obj["label_name"],
            info=external_obj["description"],
            cece_api_url="{0}{1}/".format(self.resource_uri, external_obj["id"]),
            last_updated_by=self.ceceuser,
        )
        self.assertEqual(CeceLabel.objects.filter(pk=obj.pk).exists(), True)


class CeceRemoteAPICertificateTestCase(CeceRemoteAPIBaseTestCase, APITestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.resource_uri = settings.CECE_API_URI + "mancelot/catalog/certificate/"
        self.expected_fields = [
            "id", "name", "short_description", "about", "static_url"
        ]

    def test_create_instance_with_cece_data(self):
        response = requests.get(self.resource_uri, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response_to_json(response)
        self.assertGreater(data["count"], 0)

        external_obj = data["results"][0]
        obj = Certificate.objects.create(
            name=external_obj["name"],
            info=external_obj["about"],
            cece_api_url="{0}{1}/".format(self.resource_uri, external_obj["id"]),
            last_updated_by=self.ceceuser,
        )
        self.assertEqual(Certificate.objects.filter(pk=obj.pk).exists(), True)


class CeceRemoteAPICategoryTestCase(CeceRemoteAPIBaseTestCase, APITestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.resource_uri = settings.CECE_API_URI + "mancelot/catalog/category/"
        self.expected_fields = [
            "id", "category_name", "category_ID", "type", "subcategory"
        ]

    def test_create_instance_with_cece_data(self):
        response = requests.get(self.resource_uri, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response_to_json(response)
        self.assertGreater(data["count"], 0)

        type_section_map = { v: k for k, v in dict(Category.SECTIONS).items() }
        external_obj = data["results"][0]
        obj = Category.objects.create(
            name=external_obj["category_name"],
            section=type_section_map.get(external_obj["type"], -1),  # defaults to db error
            cece_api_url="{0}{1}/".format(self.resource_uri, external_obj["id"]),
            last_updated_by=self.ceceuser,
        )
        self.assertEqual(Category.objects.filter(pk=obj.pk).exists(), True)

        # Related field: subcategory is FK
        for external_subcategory in external_obj["subcategory"]:
            sub_obj, created = Subcategory.objects.get_or_create(
                category=obj, name=external_subcategory["sub_name"],
            )
            if created:
                sub_obj.last_updated_by = self.ceceuser
                sub_obj.save()
            self.assertTrue(created)


class CeceRemoteAPIStoreTestCase(CeceRemoteAPIBaseTestCase, APITestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.resource_uri = settings.CECE_API_URI + "mancelot/catalog/store/"
        self.expected_fields = [
            "id", "store_name", "about", "store_url", "logo", "pay_methods",
        ]

    def test_create_instance_with_cece_data(self):
        response = requests.get(self.resource_uri, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response_to_json(response)
        self.assertGreater(data["count"], 0)

        external_obj = data["results"][0]
        obj = Store.objects.create(
            name=external_obj["store_name"],
            info=external_obj["about"],
            url=external_obj["store_url"],
            logo=external_obj["logo"],
            cece_api_url="{0}{1}/".format(self.resource_uri, external_obj["id"]),
            last_updated_by=self.ceceuser,
        )
        self.assertEqual(Store.objects.filter(pk=obj.pk).exists(), True)

        # Related field: pay_methods is M2M, serializes as string (name)
        for external_paymethod in external_obj["pay_methods"]:
            sub_obj, created = PaymentOption.objects.get_or_create(
                name=external_paymethod,
            )
            sub_obj.last_updated_by = self.ceceuser
            sub_obj.save()
            self.assertEqual(PaymentOption.objects.filter(pk=sub_obj.pk).exists(), True)


class CeceRemoteAPIBrandTestCase(CeceRemoteAPIBaseTestCase, APITestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.resource_uri = settings.CECE_API_URI + "mancelot/catalog/brand/"
        self.expected_fields = [
            "id", "brand_name", "about_brand", "labels", "certificate", "about_brand",
        ]

    def test_create_instance_with_cece_data(self):
        response = requests.get(self.resource_uri, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response_to_json(response)
        self.assertGreater(data["count"], 0)

        external_obj = data["results"][0]
        obj = Brand.objects.create(
            name=external_obj["brand_name"],
            info=external_obj["about_brand"],
            cece_api_url="{0}{1}/".format(self.resource_uri, external_obj["id"]),
            last_updated_by=self.ceceuser,
        )
        self.assertEqual(Brand.objects.filter(pk=obj.pk).exists(), True)

        # Related field: external labels is M2M, serializes as string (name)
        for external_label in external_obj["labels"]:
            sub_obj, created = CeceLabel.objects.get_or_create(
                name=external_label,
            )
            if created:
                sub_obj.last_updated_by = self.ceceuser
                sub_obj.save()
            self.assertEqual(CeceLabel.objects.filter(pk=sub_obj.pk).exists(), True)
        # Related field: external labels is M2M, serializes as string (name)
        for external_certificate in external_obj["certificate"]:
            sub_obj, created = Certificate.objects.get_or_create(
                name=external_certificate,
            )
            if created:
                sub_obj.last_updated_by = self.ceceuser
                sub_obj.save()
            self.assertEqual(Certificate.objects.filter(pk=sub_obj.pk).exists(), True)


class CeceRemoteAPIProductTestCase(CeceRemoteAPIBaseTestCase, APITestCase):
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

    def test_create_instance_with_cece_data(self):
        response = requests.get(self.resource_uri, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response_to_json(response)
        self.assertGreater(data["count"], 0)

        from djmoney.money import Money
        external_obj = data["results"][0]

        # Related fields: external brand and store are FK, serialized
        #     as string (brand_name, store_name)
        brand, created = Brand.objects.get_or_create(name=external_obj["brand"])
        if created:
            brand.last_updated_by = self.ceceuser; brand.save()
        store, created = Store.objects.get_or_create(name=external_obj["store"])
        if created:
            store.last_updated_by = self.ceceuser; store.save()
        # Related field: external color is a string (one color per instance)
        color, created = Color.objects.get_or_create(name=external_obj["color"])
        if created:
            color.last_updated_by = self.ceceuser; color.save()

        obj = Product.objects.create(
            name=external_obj["title"],
            info=external_obj["text"],
            extra_info=external_obj["extra_text"],
            url=external_obj["link"],

            cece_id=external_obj["productID"],
            price=Money(external_obj["price"], "EUR"),
            from_price=Money(external_obj["old_price"], "EUR") if external_obj["old_price"] else None,

            main_image=external_obj["primary_image"],
            extra_images=external_obj["extra_images"],

            brand=brand,
            store=store,

            cece_api_url="{0}{1}/".format(self.resource_uri, external_obj["id"]),
            last_updated_by=self.ceceuser,
        )
        self.assertEqual(Product.objects.filter(pk=obj.pk).exists(), True)

        # Related fields: external category (M2M) and subcategory (FK to category)
        section_map = { v: k for k, v in dict(Category.SECTIONS).items() }
        for external_category in external_obj["category"]:
            category, created = Category.objects.get_or_create(
                name=external_category,  # serializes as string (category_name)
                section=section_map["Men"],  # NB, this assumes Cece API exclusively offers data in Men section!!!
            )
            if created:
                category.last_updated_by = self.ceceuser
                category.save()
            obj.categories.add(category)
            obj.save()

        for external_subcategory in external_obj["subcategory"]:
            parent, created = Category.objects.get_or_create(
                name=external_subcategory["category"]
            )
            if created:
                parent.last_updated_by = self.ceceuser
                parent.save()
            subcategory, created = Subcategory.objects.get_or_create(
                category=parent,
                name=external_subcategory["sub_name"],
            )
            if created:
                subcategory.last_updated_by = self.ceceuser
                subcategory.save()
            obj.subcategories.add(subcategory)
            obj.save()

        for external_material in external_obj["material"]:
            material, created = Material.objects.get_or_create(
                name=external_material,  # serialized as string (name)
            )
            if created:
                material.last_updated_by = self.ceceuser
                material.save()

            obj.materials.add(material)
            obj.save()

        for external_size in external_obj["size"]:  # NB external has 'size' singular, but is M2M!
            size, created = Size.objects.get_or_create(
                name=external_size,  # serialized as string (name)
            )
            if created:
                size.last_updated_by = self.ceceuser
                size.save()

            obj.sizes.add(size)
            obj.save()
