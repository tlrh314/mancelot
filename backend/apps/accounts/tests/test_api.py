import copy
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from accounts.models import UserModel
from accounts.serializers import UserModelSerializer
from accounts.factories import (
    UserModelFactory,
    AdminFactory,
)
from catalogue.models import (
    Size,
    Store,
    Brand,
    Product,
    FavoriteProduct,
)
from catalogue.factories import (
    SizeFactory,
    StoreFactory,
    BrandFactory,
    ProductFactory,
    FavoriteProductFactory,
)
from accounts.serializers import UserFavoriteProductListSerializer


class UserModelViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls, nsizes=5, nstores=1, nbrands=1, nproducts=5):
        if Size.objects.count() < nstores:
            SizeFactory.create_batch(nsizes - Size.objects.count())
        if Store.objects.count() < nstores:
            StoreFactory.create_batch(nstores - Store.objects.count())
        if Brand.objects.count() < nbrands:
            BrandFactory.create_batch(nbrands - Brand.objects.count())
        if Product.objects.count() < nproducts:
            ProductFactory.create_batch(nproducts - Product.objects.count())

    def setUp(self):
        super().setUp()  # in case of inheritance

        # self.client = APIClient(enforce_csrf_checks=True)
        # need to login, then GET e.g. reverse("privacy_policy")
        # self.csrftoken = response.cookies["csrftoken"]
        self.csrftoken = ""

        # Obtain JSON Web Token for a superuser
        self.admin = AdminFactory(favorites__skip=True)
        self.admin.set_password("secret1234")
        self.admin.save()
        response = self.client.post(
            reverse("accounts:token_obtain_pair"), {
                "email": self.admin.email, "password": "secret1234"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admintoken= "Bearer {0}".format(response.data["access"])

        # Obtain JSON Web Token for a regular user
        self.user = UserModelFactory(favorites__skip=True)
        self.user.set_password("secret1234")
        self.user.save()
        response = self.client.post(
            reverse("accounts:token_obtain_pair"), {
                "email": self.user.email, "password": "secret1234"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.usertoken = "Bearer {0}".format(response.data["access"])

        # Unsaved UserModel instance to create via POST
        self.testuser_to_create = UserModelFactory.build(favorites__skip=True)
        self.post_data = UserModelSerializer(self.testuser_to_create).data
        self.post_data["password"] = "secret1234"

        # Saved UserModel instance to GET/PUT/PATCH/DELETE
        self.testuser_to_change = UserModelFactory.create(favorites__skip=True)
        # PUT will update all fields except the email of our testuser_to_change
        self.testuser_to_put = UserModelFactory.build(favorites__skip=True)
        self.put_data = UserModelSerializer(self.testuser_to_put).data
        self.put_data["email"] = self.testuser_to_change.email
        # PATCH will only update the zip code of our testuser_to_change
        self.patch_data = {"zip_code": "1337 XD"}

        self.list_uri = reverse("usermodel-list")
        self.detail_uri = reverse("usermodel-detail", args=[self.testuser_to_change.pk])
        self.detail_uri_me = reverse("usermodel-detail", args=["me"])

    def tearDown(self, *args, **kwargs):
        self.admin.delete()
        self.user.delete()
        super().tearDown(*args, **kwargs)

    def test_head_user_is_anonymous(self):
        response = self.client.head(self.list_uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.head(self.detail_uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.head(self.detail_uri_me)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_head_user_is_authenticated(self):
        response = self.client.head(self.list_uri,
            HTTP_AUTHORIZATION=self.usertoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # usertoken is for self.user != self.testuser_to_change, so 403!
        response = self.client.head(self.detail_uri,
            HTTP_AUTHORIZATION=self.usertoken)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # And check for me
        response = self.client.head(self.detail_uri_me,
            HTTP_AUTHORIZATION=self.usertoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_head_user_is_superuser(self):
        response = self.client.head(self.list_uri,
            HTTP_AUTHORIZATION=self.admintoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.head(self.detail_uri,
            HTTP_AUTHORIZATION=self.admintoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.head(self.detail_uri_me,
            HTTP_AUTHORIZATION=self.admintoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_options_user_is_anonymous(self):
        response = self.client.options(self.list_uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.options(self.detail_uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.options(self.detail_uri_me)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_options_user_is_authenticated(self):
        response = self.client.options(self.list_uri,
            HTTP_AUTHORIZATION=self.usertoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.options(self.detail_uri,
            HTTP_AUTHORIZATION=self.usertoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # And check for me
        response = self.client.options(self.detail_uri_me,
            HTTP_AUTHORIZATION=self.usertoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_options_user_is_superuser(self):
        response = self.client.options(self.list_uri,
            HTTP_AUTHORIZATION=self.admintoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.options(self.detail_uri,
            HTTP_AUTHORIZATION=self.usertoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.options(self.detail_uri_me,
            HTTP_AUTHORIZATION=self.usertoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_is_anonymous(self):
        response = self.client.get(self.list_uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(self.detail_uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(self.detail_uri_me)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_get_user_is_authenticated(self):
        response = self.client.get(self.list_uri,
            HTTP_AUTHORIZATION=self.usertoken)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # usertoken is for self.user != self.testuser_to_change, so 403!
        response = self.client.get(self.detail_uri,
            HTTP_AUTHORIZATION=self.usertoken)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # And check for me
        response = self.client.get(self.detail_uri_me,
            HTTP_AUTHORIZATION=self.usertoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_user_is_superuser(self):
        response = self.client.get(self.list_uri,
            HTTP_AUTHORIZATION=self.admintoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.detail_uri,
            HTTP_AUTHORIZATION=self.admintoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.detail_uri_me,
            HTTP_AUTHORIZATION=self.admintoken)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def check_assertions_for_post(self):
        user = UserModel.objects.filter(email=self.post_data["email"]).first()
        self.assertIsNotNone(user)  # user should now exist
        for k, v in self.post_data.items():
            if k == "id":
                # id is None in post_data b/c factory create does not save, so instance has no id yet
                continue
            if k == "password":  # b/c hashed
                self.assertNotEqual(getattr(user, k), v); continue
            self.assertEqual(getattr(user, k), v)
        user.delete()
    def test_post_user_is_anonymous_201(self):
        self.assertIsNone(  # user should not exist yet
            UserModel.objects.filter(email=self.post_data["email"]).first()
        )
        response = self.client.post(self.list_uri, data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.check_assertions_for_post()
    def test_post_user_is_anonymous_no_email_given_400(self):
        post_data = copy.copy(self.post_data)
        post_data.pop("email")
        response = self.client.post(self.list_uri, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)["email"][0],
            "This field is required.")
    def test_post_user_is_anonymous_no_password_given_400(self):
        post_data = copy.copy(self.post_data)
        post_data.pop("password")
        response = self.client.post(self.list_uri, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)["password"][0],
            "This field is required.")
    def test_post_user_is_anonymous_too_short_password_given_400(self):
        post_data = copy.copy(self.post_data)
        post_data["password"] = "short"
        response = self.client.post(self.list_uri, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)["password"][0],
            "Ensure this field has at least 8 characters.")
    def test_post_user_is_authenticated(self):
        self.assertIsNone(
            UserModel.objects.filter(email=self.post_data["email"]).first()
        )
        response = self.client.post(self.list_uri, data=self.post_data,
            HTTP_AUTHORIZATION=self.usertoken,
            headers={"X-CSRFToken": self.csrftoken})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.check_assertions_for_post()
    def test_post_user_is_superuser(self):
        self.assertIsNone(
            UserModel.objects.filter(email=self.post_data["email"]).first()
        )
        response = self.client.post(self.list_uri, data=self.post_data,
            HTTP_AUTHORIZATION=self.admintoken,
            headers={"X-CSRFToken": self.csrftoken}
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.check_assertions_for_post()

    def test_put_user_is_anonymous(self):
        response = self.client.put(self.detail_uri, self.put_data,
            headers={"X-CSRFToken": self.csrftoken})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_put_user_is_authenticated(self):
        response = self.client.put(self.detail_uri, self.put_data,
            HTTP_AUTHORIZATION=self.usertoken,
            headers={"X-CSRFToken": self.csrftoken})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # And check for me
        put_data = copy.copy(self.put_data)
        put_data["email"] = self.user.email
        response = self.client.put(self.detail_uri_me, put_data,
            HTTP_AUTHORIZATION=self.usertoken,
            headers={"X-CSRFToken": self.csrftoken})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_put_user_is_superuser(self):
        # First check that fields in testuser_to_change != fields in put_data
        for k, v in self.put_data.items():
            if k == "password" or k == "country" or v is None: continue
            if k == "email":
                self.assertEqual(getattr(self.testuser_to_change, k), v)
                continue
            self.assertNotEqual(getattr(self.testuser_to_change, k), v)
        response = self.client.put(self.detail_uri, self.put_data,
            HTTP_AUTHORIZATION=self.admintoken,
            headers={"X-CSRFToken": self.csrftoken})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Now check that fields in testuser_to_change are equal to fields in put_data
        testuser_to_change = UserModel.objects.get(email=self.testuser_to_change.email)
        for k, v in self.put_data.items():
            if k == "id":  continue  # b/c id is None in put_data
            if k == "password" or k == "country": continue
            self.assertEqual(getattr(testuser_to_change, k), v)

    def test_patch_user_is_anonymous(self):
        response = self.client.patch(self.detail_uri, self.patch_data,
            headers={"X-CSRFToken": self.csrftoken})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_patch_user_is_authenticated(self):
        response = self.client.patch(self.detail_uri, self.patch_data,
            HTTP_AUTHORIZATION=self.usertoken,
            headers={"X-CSRFToken": self.csrftoken})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # And check for me
        patch_data = copy.copy(self.patch_data)
        response = self.client.patch(self.detail_uri_me, patch_data,
            HTTP_AUTHORIZATION=self.usertoken,
            headers={"X-CSRFToken": self.csrftoken})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = UserModel.objects.get(email=self.user.email)
        self.assertEqual(user.zip_code, patch_data["zip_code"])
    def test_patch_user_is_superuser(self):
        response = self.client.patch(self.detail_uri, self.patch_data,
            HTTP_AUTHORIZATION=self.admintoken,
            headers={"X-CSRFToken": self.csrftoken})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        testuser_to_change = UserModel.objects.get(email=self.testuser_to_change.email)
        self.assertEqual(testuser_to_change.zip_code, self.patch_data["zip_code"])

    def test_delete_user_is_anonymous(self):
        response = self.client.delete(self.detail_uri,
            headers={"X-CSRFToken": self.csrftoken})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_delete_user_is_authenticated(self):
        response = self.client.delete(self.detail_uri,
            HTTP_AUTHORIZATION=self.usertoken,
            headers={"X-CSRFToken": self.csrftoken})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # And check for me --> we do not allow users to delete themselves
        response = self.client.delete(self.detail_uri_me,
            HTTP_AUTHORIZATION=self.usertoken,
            headers={"X-CSRFToken": self.csrftoken})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_delete_user_is_superuser(self):
        response = self.client.delete(self.detail_uri,
            HTTP_AUTHORIZATION=self.admintoken,
            headers={"X-CSRFToken": self.csrftoken})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(
            UserModel.objects.filter(email=self.testuser_to_change.email).first()
        )

    def test_get_favorites(self):
        for product in Product.objects.order_by("?")[0:5]:
            fav = FavoriteProductFactory(
                product=product, user=self.user, size=product.sizes.order_by("?").first()

            )
        self.assertEqual(self.user.favorites.count(), 5)
        response = self.client.get(reverse("usermodel-favorites", args=["me"]),
            HTTP_AUTHORIZATION=self.usertoken
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.favorites.count(), 5)
        self.assertEqual(response.data, UserFavoriteProductListSerializer(self.user.favorites.all(), many=True).data)

    def test_post_favorites(self):
        response = self.client.post(reverse("usermodel-favorites", args=["me"]),
            HTTP_AUTHORIZATION=self.usertoken
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_favorites(self):
        response = self.client.put(reverse("usermodel-favorites", args=["me"]),
            HTTP_AUTHORIZATION=self.usertoken
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_add_favorite(self):
        product = Product.objects.first()
        size = product.sizes.order_by("?").first()
        self.assertEqual(self.user.favorites.count(), 0)
        with self.subTest("Product exists MancelotAlpha0-9"):
            response = self.client.patch(
                reverse("usermodel-favorites", args=["me"]),
                {"product_id": product.id, "quantity": 3},
                HTTP_AUTHORIZATION=self.usertoken
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["status"], "Favorite added")
            self.assertEqual(self.user.favorites.count(), 1)
            self.assertEqual(self.user.favorites.first().quantity, 3)
        with self.subTest("Product exists post-MancelotAlpha0-9: size_id given"):
            response = self.client.patch(
                reverse("usermodel-favorites", args=["me"]),
                {"product_id": product.id, "size_id": size.id, "quantity": 3},
                HTTP_AUTHORIZATION=self.usertoken
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["status"], "Favorite added")
            self.assertEqual(self.user.favorites.count(), 1)
            self.assertEqual(self.user.favorites.first().quantity, 3)
        with self.subTest("Product does not exist MancelotAlpha0-9"):
            response = self.client.patch(
                reverse("usermodel-favorites", args=["me"]),
                {"product_id": -1, "quantity": 3},
                HTTP_AUTHORIZATION=self.usertoken
            )
            self.assertEqual(response.data["status"], "Product does not exist")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        with self.subTest("Product does not exist post-MancelotAlpha0-9: size_id given"):
            response = self.client.patch(
                reverse("usermodel-favorites", args=["me"]),
                {"product_id": -1, "size_id": size.id, "quantity": 3},
                HTTP_AUTHORIZATION=self.usertoken
            )
            self.assertEqual(response.data["status"], "Product does not exist")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        with self.subTest("Incorrect Field MancelotAlpha0-9"):
            response = self.client.patch(
                reverse("usermodel-favorites", args=["me"]),
                # TODO: add size_id once it is required
                {"product": -1, "quantity": 3},
                HTTP_AUTHORIZATION=self.usertoken
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        with self.subTest("Incorrect Type in Field MancelotAlpha0-9"):
            response = self.client.patch(
                reverse("usermodel-favorites", args=["me"]),
                # TODO: add size_id  once it is required
                {"product": "sjenkie", "quantity": 3},
                HTTP_AUTHORIZATION=self.usertoken
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_favorite(self):
        product = Product.objects.order_by("?").first()
        fav = FavoriteProduct.objects.create(
            product=product, user=self.user, quantity=3
        )
        self.assertEqual(self.user.favorites.count(), 1)
        self.assertEqual(self.user.favorites.first().quantity, 3)
        with self.subTest("Product exists"):
            response = self.client.delete(
                reverse("usermodel-favorites", args=["me"]),
                {"product_id": product.id},
                HTTP_AUTHORIZATION=self.usertoken
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["status"], "Favorite deleted")
            self.assertEqual(self.user.favorites.count(), 0)
        with self.subTest("Product does not exist"):
            response = self.client.delete(
                reverse("usermodel-favorites", args=["me"]),
                {"product_id": -1},
                HTTP_AUTHORIZATION=self.usertoken
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        with self.subTest("Incorrect Field"):
            response = self.client.delete(
                reverse("usermodel-favorites", args=["me"]),
                {"product": -1},
                HTTP_AUTHORIZATION=self.usertoken
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        with self.subTest("Incorrect Type in Field"):
            response = self.client.delete(
                reverse("usermodel-favorites", args=["me"]),
                {"product": "sjenkie"},
                HTTP_AUTHORIZATION=self.usertoken
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
