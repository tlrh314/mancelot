from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
    APISimpleTestCase,
    APITransactionTestCase,
    APILiveServerTestCase,
    APIRequestFactory
)

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
from accounts.factories import (
    UserModelFactory,
    AdminFactory,
)


class CatalogueAPIBaseTestCase(object):
    def setUp(self):
        super().setUp()  # in case of inheritance

        # Obtain JSON Web Token for a superuser
        self.admin = AdminFactory(favorites__skip=True)
        self.admin.set_password("secret")
        self.admin.save()
        response = self.client.post(
            reverse("accounts:token_obtain_pair"), {
                "email": self.admin.email, "password": "secret"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admintoken= "Bearer {0}".format(response.data["access"])

        # Obtain JSON Web Token for a regular user
        self.user = UserModelFactory(favorites__skip=True)
        self.user.set_password("secret")
        self.user.save()
        response = self.client.post(
            reverse("accounts:token_obtain_pair"), {
                "email": self.user.email, "password": "secret"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.usertoken = "Bearer {0}".format(response.data["access"])

    def tearDown(self, *args, **kwargs):
        self.admin.delete()
        self.user.delete()
        super().tearDown(*args, **kwargs)

    ### HEAD requests --> allowed for anon, user and admin
    def test_head_list_user_is_anonymous_200(self):
        response = self.client.head(reverse(self.list_uri))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Allow"], "GET, HEAD, OPTIONS")
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response["Vary"], "Accept, Accept-Language, Cookie")

        response = self.client.head(reverse(self.detail_uri, args=[self.detail_pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Allow"], "GET, HEAD, OPTIONS")
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response["Vary"], "Accept, Accept-Language, Cookie")

    def test_head_user_is_authenticated_200(self):
        response = self.client.head(
            reverse(self.list_uri),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.head(
            reverse(self.detail_uri, args=[self.detail_pk]),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_head_user_is_superuser_200(self):
        response = self.client.head(
            reverse(self.list_uri),
            HTTP_AUTHORIZATION=self.admintoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.head(
            reverse(self.detail_uri, args=[self.detail_pk]),
            HTTP_AUTHORIZATION=self.admintoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    ### OPTIONS requests --> allowed for anon, user and admin
    def verify_options_data(self, response):
        self.assertIn("name", response.data.keys())
        self.assertIsInstance(response.data["name"], str)
        self.assertIn("description", response.data.keys())
        self.assertIsInstance(response.data["description"], str)
        self.assertIn("renders", response.data.keys())
        self.assertIn("application/json", response.data["renders"])
        self.assertIn("text/html", response.data["renders"])
        self.assertIsInstance(response.data["renders"], list)
        self.assertIn("parses", response.data.keys())
        self.assertIsInstance(response.data["parses"], list)
        self.assertIn("application/json", response.data["parses"])
        self.assertIn("application/x-www-form-urlencoded", response.data["parses"])
        self.assertIn("multipart/form-data", response.data["parses"])

    def test_options_user_is_anonymous_200(self):
        response = self.client.options(reverse(self.list_uri))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.verify_options_data(response)
        self.assertEqual(response.data["name"], self.resource_name_list)  # Sanity check

        response = self.client.options(
            reverse(self.detail_uri, args=[self.detail_pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.resource_name_detail)  # Sanity check
        self.verify_options_data(response)

    def test_options_user_is_authenticated_200(self):
        response = self.client.options(
            reverse(self.list_uri),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.options(
            reverse(self.detail_uri, args=[self.detail_pk]),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_options_user_is_superuser(self):
        response = self.client.options(
            reverse(self.list_uri),
            HTTP_AUTHORIZATION=self.admintoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.options(
            reverse(self.detail_uri, args=[self.detail_pk]),
            HTTP_AUTHORIZATION=self.admintoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    ### GET requests --> allowed for anon, user and admin
    def verify_get_response_data_results(self, data_api, data_orm):
        """ Verify that the 'actual' data in the list/detail response is correct """
        self.assertEqual(len(data_api.keys()), len(self.serializer_fields))
        self.assertEqual(list(data_api.keys()), self.serializer_fields)
        for field in self.serializer_fields:
            # TODO: handle FK and M2M
            print("\n{0}\napi -> {1}: {2}\norm -> {3}: {4}".format(
                field, data_api[field], type(data_api[field]),
                getattr(data_orm, field), type(getattr(data_orm, field))
            ))
            self.assertEqual(data_api[field], getattr(data_orm, field))

    def verify_get_list_response_data(self, response):
        self.assertIn("count", response.data.keys())
        self.assertIn("next", response.data.keys())
        self.assertIn("previous", response.data.keys())
        self.assertIn("results", response.data.keys())

        self.assertEqual(response.data["count"], self.count)
        data_api = response.data["results"][0]
        self.verify_get_response_data_results(data_api, self.data_orm)

    def verify_get_detail_response_data(self, response):
        data_api = response.data
        self.verify_get_response_data_results(data_api, self.data_orm_detail)

    def test_get_user_is_anonymous_200(self):
        response = self.client.get(reverse(self.list_uri))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.verify_get_list_response_data(response)

        response = self.client.get(reverse(self.detail_uri, args=[self.detail_pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.verify_get_detail_response_data(response)

    def test_get_user_is_authenticated_200(self):
        response = self.client.get(
            reverse(self.list_uri),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.verify_get_list_response_data(response)

        response = self.client.get(
            reverse(self.detail_uri, args=[self.detail_pk]),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.verify_get_detail_response_data(response)

    def test_get_user_is_superuser_200(self):
        response = self.client.get(
            reverse(self.list_uri),
            HTTP_AUTHORIZATION=self.admintoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.verify_get_list_response_data(response)

        response = self.client.get(
            reverse(self.detail_uri, args=[self.detail_pk]),
            HTTP_AUTHORIZATION=self.admintoken,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.verify_get_detail_response_data(response)

    ### POST requests --> disabled for anon, user and admin
    def test_post_user_is_anonymous_401(self):
        response = self.client.post(reverse(self.list_uri))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(reverse(self.detail_uri, args=[self.detail_pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_user_is_authenticated_405(self):
        response = self.client.post(
            reverse(self.list_uri),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.post(
            reverse(self.detail_uri, args=[self.detail_pk]),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_user_is_superuser(self):
        response = self.client.post(
            reverse(self.list_uri),
            HTTP_AUTHORIZATION=self.admintoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.post(
            reverse(self.detail_uri, args=[self.detail_pk]),
            HTTP_AUTHORIZATION=self.admintoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    ### PUT requests --> disabled for anon, user and admin
    def test_put_user_is_anonymous_401(self):
        response = self.client.put(reverse(self.list_uri))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(reverse(self.detail_uri, args=[self.detail_pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_user_is_authenticated_405(self):
        response = self.client.put(
            reverse(self.list_uri),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(
            reverse(self.detail_uri, args=[self.detail_pk]),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_user_is_superuser_405(self):
        response = self.client.put(
            reverse(self.list_uri),
            HTTP_AUTHORIZATION=self.admintoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(
            reverse(self.detail_uri, args=[self.detail_pk]),
            HTTP_AUTHORIZATION=self.admintoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    ### PATCH requests --> disabled for anon, user and admin
    def test_patch_user_is_anonymous_401(self):
        response = self.client.patch(reverse(self.list_uri))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(reverse(self.detail_uri, args=[self.detail_pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_user_is_authenticated_405(self):
        response = self.client.patch(
            reverse(self.list_uri),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.post(
            reverse(self.detail_uri, args=[self.detail_pk]),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_user_is_superuser_405(self):
        response = self.client.patch(
            reverse(self.list_uri),
            HTTP_AUTHORIZATION=self.admintoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.post(
            reverse(self.detail_uri, args=[self.detail_pk]),
            HTTP_AUTHORIZATION=self.admintoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    ### DELETE requests --> disabled for anon, user and admin
    def test_delete_user_is_anonymous_401(self):
        response = self.client.delete(reverse(self.list_uri))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(reverse(self.detail_uri, args=[self.detail_pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_is_authenticated_405(self):
        response = self.client.delete(
            reverse(self.list_uri),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(
            reverse(self.detail_uri, args=[self.detail_pk]),
            HTTP_AUTHORIZATION=self.usertoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_user_is_superuser_405(self):
        response = self.client.delete(
            reverse(self.list_uri),
            HTTP_AUTHORIZATION=self.admintoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(
            reverse(self.detail_uri, args=[self.detail_pk]),
            HTTP_AUTHORIZATION=self.admintoken,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class CeceLabelViewSetTest(CatalogueAPIBaseTestCase, APITestCase):
    @classmethod
    def setUpTestData(cls):
        # TODO: fixtures
        if CeceLabel.objects.count() < 5:
            CeceLabelFactory.create_batch(5 - CeceLabel.objects.count())

    def setUp(self):
        # Set the admin + user tokens
        super().setUp()

        # Set the detail for this specific test
        self.list_uri = "cecelabel-list"
        self.detail_uri = "cecelabel-detail"
        self.detail_pk = CeceLabel.objects.last().pk
        self.count = CeceLabel.objects.count()
        self.data_orm = CeceLabel.objects.order_by("name").first()
        self.data_orm_detail = CeceLabel.objects.get(pk=self.detail_pk)  # last()
        self.serializer_fields = ["id", "name", "slug", "info"]
        self.resource_name_list = "Cece Label List"
        self.resource_name_detail = "Cece Label Instance"


class CertificateViewSetTest(CatalogueAPIBaseTestCase, APITestCase):
    @classmethod
    def setUpTestData(cls):
        # TODO: fixtures
        if Certificate.objects.count() < 20:
            CertificateFactory.create_batch(20 - Certificate.objects.count())


    def setUp(self):
        # Set the admin + user tokens
        super().setUp()

        # Set the detail for this specific test
        self.list_uri = "certificate-list"
        self.detail_uri = "certificate-detail"
        self.detail_pk = Certificate.objects.last().pk
        self.count = Certificate.objects.count()
        self.data_orm = Certificate.objects.order_by("name").first()
        self.data_orm_detail = Certificate.objects.get(pk=self.detail_pk)  # last()
        self.serializer_fields = ["id", "name", "slug", "info"]
        self.resource_name_list = "Certificate List"
        self.resource_name_detail = "Certificate Instance"


class CategoryViewSetTest(CatalogueAPIBaseTestCase, APITestCase):
    @classmethod
    def setUpTestData(cls):
        # TODO: fixtures
        if Category.objects.count() < 20:
            CategoryFactory.create_batch(20 - Category.objects.count(),
                subcategories__skip=True)

    def setUp(self):
        # Set the admin + user tokens
        super().setUp()

        # Set the detail for this specific test
        self.list_uri = "category-list"
        self.detail_uri = "category-detail"
        self.detail_pk = Category.objects.last().pk
        self.count = Category.objects.count()
        self.data_orm = Category.objects.order_by("name").first()
        self.data_orm_detail = Category.objects.get(pk=self.detail_pk)  # last()
        self.serializer_fields = ["id", "name", "slug", "section", "subcategories"]
        self.resource_name_list = "Category List"
        self.resource_name_detail = "Category Instance"


class SubcategoryViewSetTest(CatalogueAPIBaseTestCase, APITestCase):
    @classmethod
    def setUpTestData(cls):
        # TODO: fixtures
        if Subcategory.objects.count() < 20:
            SubcategoryFactory.create_batch(20 - Subcategory.objects.count())

    def setUp(self):
        # Set the admin + user tokens
        super().setUp()

        # Set the detail for this specific test
        self.list_uri = "subcategory-list"
        self.detail_uri = "subcategory-detail"
        self.detail_pk = Subcategory.objects.last().pk
        self.count = Subcategory.objects.count()
        self.data_orm = Subcategory.objects.order_by("name").first()
        self.data_orm_detail = Subcategory.objects.get(pk=self.detail_pk)  # last()
        self.serializer_fields = ["id", "name", "slug", "category"]
        self.resource_name_list = "Subcategory List"
        self.resource_name_detail = "Subcategory Instance"


class PaymentOptionViewSetTest(CatalogueAPIBaseTestCase, APITestCase):
    @classmethod
    def setUpTestData(cls):
        # TODO: fixtures
        if PaymentOption.objects.count() < 20:
            PaymentOptionFactory.create_batch(20 - PaymentOption.objects.count())

    def setUp(self):
        # Set the admin + user tokens
        super().setUp()

        # Set the detail for this specific test
        self.list_uri = "paymentoption-list"
        self.detail_uri = "paymentoption-detail"
        self.detail_pk = PaymentOption.objects.last().pk
        self.count = PaymentOption.objects.count()
        self.data_orm = PaymentOption.objects.order_by("name").first()
        self.data_orm_detail = PaymentOption.objects.get(pk=self.detail_pk)  # last()
        self.serializer_fields = ["id", "name", "slug", "logo"]
        self.resource_name_list = "Payment Option List"
        self.resource_name_detail = "Payment Option Instance"


class StoreViewSetTest(CatalogueAPIBaseTestCase, APITestCase):
    @classmethod
    def setUpTestData(cls):
        if Store.objects.count() < 40:
            StoreFactory.create_batch(40 - Store.objects.count())

    def setUp(self):
        # Set the admin + user tokens
        super().setUp()

        # Set the detail for this specific test
        self.list_uri = "store-list"
        self.detail_uri = "store-detail"
        self.detail_pk = Store.objects.last().pk
        self.count = Store.objects.count()
        self.data_orm = Store.objects.order_by("name").first()
        self.data_orm_detail = Store.objects.get(pk=self.detail_pk)  # last()
        self.serializer_fields = [
            "id", "name", "slug", "info", "url", "logo", "payment_options",
        ]
        self.resource_name_list = "Store List"
        self.resource_name_detail = "Store Instance"


class BrandViewSetTest(CatalogueAPIBaseTestCase, APITestCase):
    @classmethod
    def setUpTestData(cls):
        if Brand.objects.count() < 100:
            BrandFactory.create_batch(100 - Brand.objects.count())

    def setUp(self):
        # Set the admin + user tokens
        super().setUp()

        # Set the detail for this specific test
        self.list_uri = "brand-list"
        self.detail_uri = "brand-detail"
        self.detail_pk = Brand.objects.last().pk
        self.count = Brand.objects.count()
        self.data_orm = Brand.objects.order_by("name").first()
        self.data_orm_detail = Brand.objects.get(pk=self.detail_pk)  # last()
        self.serializer_fields = [
            "id", "name", "slug", "info", "url", "logo",
            "labels", "certificates"
        ]
        self.resource_name_list = "Brand List"
        self.resource_name_detail = "Brand Instance"


class SizeViewSet(CatalogueAPIBaseTestCase, APITestCase):
    @classmethod
    def setUpTestData(cls):
        if Size.objects.count() < 50:
            SizeFactory.create_batch(50 - Size.objects.count())

    def setUp(self):
        # Set the admin + user tokens
        super().setUp()

        # Set the detail for this specific test
        self.list_uri = "size-list"
        self.detail_uri = "size-detail"
        self.detail_pk = Size.objects.last().pk
        self.count = Size.objects.count()
        self.data_orm = Size.objects.order_by("name").first()
        self.data_orm_detail = Size.objects.get(pk=self.detail_pk)  # last()
        self.serializer_fields = ["id", "name", "slug"]
        self.resource_name_list = "Size List"
        self.resource_name_detail = "Size Instance"


class ColorViewSetTest(CatalogueAPIBaseTestCase, APITestCase):
    @classmethod
    def setUpTestData(cls):
        if Color.objects.count() < 50:
            ColorFactory.create_batch(50 - Color.objects.count())

    def setUp(self):
        # Set the admin + user tokens
        super().setUp()

        # Set the detail for this specific test
        self.list_uri = "color-list"
        self.detail_uri = "color-detail"
        self.detail_pk = Color.objects.last().pk
        self.count = Color.objects.count()
        self.data_orm = Color.objects.order_by("name").first()
        self.data_orm_detail = Color.objects.get(pk=self.detail_pk)  # last()
        self.serializer_fields = ["id", "name", "slug"]
        self.resource_name_list = "Color List"
        self.resource_name_detail = "Color Instance"


class MaterialViewSetTest(CatalogueAPIBaseTestCase, APITestCase):
    @classmethod
    def setUpTestData(cls):
        if Material.objects.count() < 50:
            MaterialFactory.create_batch(50 - Material.objects.count())

    def setUp(self):
        # Set the admin + user tokens
        super().setUp()

        # Set the detail for this specific test
        self.list_uri = "material-list"
        self.detail_uri = "material-detail"
        self.detail_pk = Material.objects.last().pk
        self.count = Material.objects.count()
        self.data_orm = Material.objects.order_by("name").first()
        self.data_orm_detail = Material.objects.get(pk=self.detail_pk)  # last()
        self.serializer_fields = ["id", "name", "slug", "info"]
        self.resource_name_list = "Material List"
        self.resource_name_detail = "Material Instance"


class ProductViewSetTest(CatalogueAPIBaseTestCase, APITestCase):
    @classmethod
    def setUpTestData(cls):
        if Store.objects.count() < 5:
            StoreFactory.create_batch(5 - Store.objects.count())
        if Brand.objects.count() < 10:
            BrandFactory.create_batch(10 - Brand.objects.count())
        if Product.objects.count() < 50:
            ProductFactory.create_batch(50 - Product.objects.count())

    def setUp(self):
        # Set the admin + user tokens
        super().setUp()

        # Set the detail for this specific test
        self.list_uri = "product-list"
        self.detail_uri = "product-detail"
        self.detail_pk = Product.objects.last().pk
        self.count = Product.objects.count()
        self.data_orm = Product.objects.order_by("name").first()
        self.data_orm_detail = Product.objects.get(pk=self.detail_pk)  # last()
        self.serializer_fields = [
            "id", "name", "slug", "info", "extra_info", "url", "cece_id",
            "price", "price_currency", "from_price", "from_price_currency",
            "main_image", "extra_images", "brand", "store",
            "categories", "subcategories", "materials",
            "sizes", "colors",
        ]
        self.resource_name_list = "Product List"
        self.resource_name_detail = "Product Instance"
