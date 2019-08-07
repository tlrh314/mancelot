import json

from django.test import (
    RequestFactory,
    TestCase,
    Client
)
from django.urls import reverse
from rest_framework import status

from accounts.models import UserModel
from accounts.serializers import UserModelSerializer



class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/customer/details')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = my_view(request)
        # Use this syntax for class-based views.
        response = MyView.as_view()(request)
        self.assertEqual(response.status_code, 200)






client = Client()


class GetAllUserModelInstancesTest(TestCase):
    """ Test module for GET all UserModel instances API """

    def setUp(self):
        UserModel.objects.create(
            email="casper@example.com", full_name="Casper"
        )
        UserModel.objects.create(
            email="muffin@example.com", full_name="Muffin"
        )
        UserModel.objects.create(
            email="rambo@example.com", full_name="Rambo"
        )

    def test_get_all_usermodel_instances_fails_to_return_data(self):
        response = client.get(reverse("get_post_puppies"))
        self.assertEqual(response.status_code, status.HTTP_400_OK)


class GetSingleUserModelInstanceTest(TestCase):
    """ Test module for GET single puppy API """

    def setUp(self):
        self.casper = UserModel.objects.create(
            email="casper@example.com", full_name="Casper"
        )
        self.muffin = UserModel.objects.create(
            email="muffin@example.com", full_name="Muffin"
        )
        self.rambo = UserModel.objects.create(
            email="rambo@example.com", full_name="Rambo"
        )

    def test_get_valid_single_user(self):
        response = client.get(
            reverse("get_post_puppies", kwargs={"pk": self.rambo.pk})
        )
        user = UserModel.objects.first()
        serializer = UserModelSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_user(self):
        response = client.get(
            reverse("get_delete_update_puppy", kwargs={"pk": 42})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewUserModelInstanceTest(TestCase):
    """ Test module for inserting a new UserModel instance """

    def setUp(self):
        self.valid_payload = {
            "email": "muffin@example.com",
            "full_name": "Muffin",
        }
        self.valid_payload_with_address = {
            "email": "muffin@example.com",
            "full_name": "Muffin",
            # TODO
        }
        self.invalid_payload = {
            "email": "muffin@example.com",
            "full_name": "",
        }

    def test_create_valid_user(self):
        response = client.post(
            reverse("get_post_puppies"),
            data=json.dumps(self.valid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = client.post(
            reverse("get_post_puppies"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleUserModelInstanceTest(TestCase):
    """ Test module for updating an existing UserModel record """

    def setUp(self):
        self.casper = UserModel.objects.create(
            email="casper@example.com", full_name="Casper"
        )
        self.muffin = UserModel.objects.create(
            email="muffin@example.com", full_name="Muffin"
        )
        self.valid_payload_data_unchanged = {
            "email": "muffin@example.com",
            "full_name": "Muffin",
        }
        self.valid_payload_full_name_updated = {
            "email": "muffin@example.com",
            "full_name": "Blueberry Muffin",
        }
        self.invalid_payload = {
            "email": "muffin@example.com",
            "full_name": "",
        }

    def test_valid_update_user_unchanged(self):
        response = client.put(
            reverse("get_delete_update_puppy", kwargs={"pk": self.muffin.pk}),
            data=json.dumps(self.valid_payload_data_unchanged),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_valid_update_user_did_change(self):
        response = client.put(
            reverse("get_delete_update_puppy", kwargs={"pk": self.muffin.pk}),
            data=json.dumps(self.valid_payload_full_name_updated),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        muffin_updated = UserModel.objects.get(pk=self.muffin.pk)
        self.assertEqual(muffin_updated.full_name, self.valid_payload_full_name_updated["full_name"])

    def test_invalid_update_user(self):
        response = client.put(
            reverse("get_delete_update_puppy", kwargs={"pk": self.muffin.pk}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleUserModelInstanceTest(TestCase):
    """ Test module for deleting an existing UserModel record """

    def setUp(self):
        self.casper = UserModel.objects.create(
            email="casper@example.com", full_name="Casper"
        )
        self.muffin = UserModel.objects.create(
            email="casper@example.com", full_name="Muffin",
        )

    def test_valid_delete_puppy(self):
        response = client.delete(
            reverse("get_delete_update_puppy", kwargs={"pk": self.muffin.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_puppy(self):
        response = client.delete(
            reverse("get_delete_update_puppy", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
