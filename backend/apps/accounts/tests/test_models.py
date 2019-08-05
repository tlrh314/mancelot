from django.test import TestCase
from django.core.exceptions import ValidationError

from accounts.models import UserModel


class UserModelTest(TestCase):

    def test_new_user_is_not_active(self):
        user = UserModel(
            email="timo@mancelot.nl",
            full_name="Timo Halbesma",
        )
        self.assertEqual(user.is_active, False)

    def test_new_user_is_not_staff(self):
        user = UserModel(
            email="timo@mancelot.nl",
            full_name="Timo Halbesma",
        )
        self.assertEqual(user.is_staff, False)

    def test_new_user_is_not_superuser(self):
        user = UserModel(
            email="timo@mancelot.nl",
            full_name="Timo Halbesma",
        )
        self.assertEqual(user.is_superuser, False)

    def test_new_empty_user_raises_validation_error(self):
        user = UserModel.objects.create()
        self.assertRaises(ValidationError, user.clean)

    def test_verbose_name_singular(self):
        self.assertEqual(str(UserModel._meta.verbose_name), "User")

    def test_verbose_name_plural(self):
        self.assertEqual(str(UserModel._meta.verbose_name_plural), "Users")

    def test_string_representation(self):
        user = UserModel(
            email="timo@mancelot.nl",
            full_name="Timo Halbesma",
        )
        self.assertEqual(str(user), "{0} ({1})".format(user.full_name, user.email))

    def test_user_with_address(self):
        user = UserModel(
            email="timo@mancelot.nl",
            full_name="Timo Halbesma",
            address="Straatnaam 42",
            zip_code="1337 XD",
            country="NL"
        )
        self.assertEqual(user.email, "timo@mancelot.nl")
        self.assertEqual(user.full_name, "Timo Halbesma")
        self.assertEqual(user.address, "Straatnaam 42")
        self.assertEqual(user.country, "NL")

    def test_save_new_usermodel_instance(self):
        user = UserModel(
            email="timo@mancelot.nl",
            full_name="Timo Halbesma",
        )
        user.save()
        self.assertEqual(UserModel.objects.last(), user)

    def test_send_email_to_user(self):
        # user = UserModel(
        #     email="timo@mancelot.nl",
        #     full_name="Timo Halbesma",
        # )
        # user.email_user(subject, message, from_email=settings.DEFAULT_FROM_EMAIL)
        pass
