from django.test import (
    RequestFactory,
    TestCase,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

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
from catalogue.api import (
    CeceLabelViewSet,
    CertificateViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    PaymentOptionViewSet,
    StoreViewSet,
    BrandViewSet,
    SizeViewSet,
    ColorViewSet,
    MaterialViewSet,
    ProductViewSet
)
from accounts.factories import AdminFactory


class BaseTestCase(TestCase):
    def setUp(self):
        csrf_client = APIClient(enforce_csrf_checks=True)

        admin = AdminFactory(favorites__skip=True)
        admin.set_password("secret")
        admin.save()
        response = csrf_client.post(
            reverse("accounts:token_obtain_pair"), {
                "email": admin.email, "password": "secret"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admintoken= "Bearer {0}".format(response.data["access"])

        user = AdminFactory(favorites__skip=True)
        user.set_password("secret")
        user.save()
        response = csrf_client.post(
            reverse("accounts:token_obtain_pair"), {
                "email": user.email, "password": "secret"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.usertoken = "Bearer {0}".format(response.data["access"])


class CeceLabelViewSetTest(BaseTestCase):
    def setUp(self):
        if CeceLabel.objects.count() < 5:
            CeceLabelFactory.create_batch(5 - CeceLabel.objects.count())

        super().setUp()

    def test_head_cecelabel_list_user_is_anonymous_200(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        response = csrf_client.head(reverse("cecelabel-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = csrf_client.head(
            reverse("cecelabel-detail", args=[CeceLabel.objects.first().pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_head_cecelabel_user_is_authenticated_200(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        response = csrf_client.head(
            reverse("cecelabel-list"),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = csrf_client.head(
            reverse("cecelabel-detail", args=[CeceLabel.objects.first().pk]),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_options_cecelabel_user_is_anonymous_200(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        response = csrf_client.get(reverse("cecelabel-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = csrf_client.get(
            reverse("cecelabel-detail", args=[CeceLabel.objects.first().pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_options_cecelabel_user_is_authenticated_200(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        response = csrf_client.options(
            reverse("cecelabel-list"),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = csrf_client.options(
            reverse("cecelabel-detail", args=[CeceLabel.objects.first().pk]),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_cecelabel_user_is_anonymous_200(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        response = csrf_client.get(reverse("cecelabel-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = csrf_client.get(
            reverse("cecelabel-detail", args=[CeceLabel.objects.first().pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_cecelabel_user_is_authenticated_200(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        response = csrf_client.get(
            reverse("cecelabel-list"),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = csrf_client.get(
            reverse("cecelabel-detail", args=[CeceLabel.objects.first().pk]),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_post_cecelabel_user_is_anonymous_405(self):
#         status.HTTP_405_METHOD_NOT_ALLOWED
#         pass
#     def test_post_cecelabel_user_is_authenticated_405(self):
#         pass
#     def test_put_cecelabel_user_is_anonymous_405(self):
#         pass
#     def test_put_cecelabel_user_is_authenticated_405(self):
#         pass
#     def test_patch_cecelabel_user_is_anonymous_405(self):
#         pass
#     def test_patch_cecelabel_user_is_authenticated_405(self):
#         pass
#     def test_delete_cecelabel_user_is_anonymous_405(self):
#         pass
#     def test_delete_cecelabel_user_is_authenticated_405(self):
#         pass
#
#
# class CertificateViewSet(BaseTestCase):
#     pass
#
# class CategoryViewSetTest(BaseTestCase):
#     pass
#
#
# class SubcategoryViewSetTest(BaseTestCase):
#     pass
#
#
# class PaymentOptionViewSetTest(BaseTestCase):
#     pass
#
#
# class StoreViewSetTest(BaseTestCase):
#     pass
#
#
# class BrandViewSetTest(BaseTestCase):
#     pass
#
#
# class SizeViewSet(BaseTestCase):
#     pass
#
#
# class ColorViewSetTest(BaseTestCase):
#     pass
#
#
# class MaterialViewSetTest(BaseTestCase):
#     pass
#
#
# class ProductViewSetTest(BaseTestCase):
#     pass
