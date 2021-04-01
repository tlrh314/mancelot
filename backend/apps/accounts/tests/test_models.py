from django.test import TestCase
from django.utils import translation
from django.core.exceptions import ValidationError

from accounts.models import UserModel
from accounts.factories import AdminFactory, UserModelFactory


class UserModelTest(TestCase):
    def test_verbose_name(self):
        translation.activate("en")
        self.assertEqual(str(UserModel._meta.verbose_name), "User")
        self.assertEqual(str(UserModel._meta.verbose_name_plural), "Users")
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_field_names(self):
        translation.activate("en")
        self.assertEqual(UserModel._meta.get_field("email").verbose_name, "email")
        self.assertEqual(
            UserModel._meta.get_field("full_name").verbose_name, "full name"
        )
        self.assertEqual(UserModel._meta.get_field("address").verbose_name, "address")
        self.assertEqual(UserModel._meta.get_field("zip_code").verbose_name, "zip code")
        self.assertEqual(UserModel._meta.get_field("city").verbose_name, "city")
        self.assertEqual(UserModel._meta.get_field("country").verbose_name, "country")

        self.assertEqual(
            UserModel._meta.get_field("favorites").verbose_name, "favorites"
        )

        self.assertEqual(UserModel._meta.get_field("balance").verbose_name, "balance")
        self.assertEqual(
            UserModel._meta.get_field("monthly_top_up").verbose_name, "monthly top up"
        )
        self.assertEqual(
            UserModel._meta.get_field("payment_preference").verbose_name,
            "payment preference",
        )

        self.assertEqual(UserModel._meta.get_field("is_active").verbose_name, "active")
        self.assertEqual(UserModel._meta.get_field("is_staff").verbose_name, "staff")
        self.assertEqual(
            UserModel._meta.get_field("is_superuser").verbose_name, "superuser"
        )
        # TODO: translation.activate("nl"), then run checks for translated field names

    def test_save_method_of_new_usermodel_instance(self):
        user = UserModelFactory(
            email="timo@mancelot.app",
            full_name="Timo Halbesma",
            favorites__skip=True,
        )
        user.save()
        self.assertEqual(UserModel.objects.last(), user)
        user.delete()

    def test_new_user_is_not_active(self):
        user = UserModel.objects.create(
            email="timo@mancelot.app",
            full_name="Timo Halbesma",
        )
        self.assertEqual(user.is_active, False)
        user.delete()

    def test_new_user_is_not_staff_is_not_superuser(self):
        user = UserModel.objects.create(
            email="timo@mancelot.app",
            full_name="Timo Halbesma",
        )
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        user.delete()

    def test_new_user_from_factory_is_not_staff_and_not_superuser(self):
        user = UserModelFactory.build(favorites__skip=True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)

    def test_new_admin_from_factory_is_staff_and_superuser(self):
        user = AdminFactory.build(favorites__skip=True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)

    def test_new_empty_user_raises_validation_error(self):
        self.assertRaises(ValidationError, UserModel().save())

    def test_new_user_with_nonunique_email_raises_validation_error(self):
        user1 = UserModelFactory(
            email="timo@mancelot.app",
            full_name="Timo Halbesma",
            favorites__skip=True,
        )
        user2 = UserModelFactory.build(email=user1.email, favorites__skip=True)
        # TODO: this may actually raise an IntegrityError (i.e. already commiting to database. BAD)
        # Possibly have to check the clean method?
        self.assertRaises(ValidationError, user2.save())
        user1.delete()
        user2.delete()

    def test_verbose_name_singular(self):
        self.assertEqual(str(UserModel._meta.verbose_name), "User")
        self.assertEqual(str(UserModel._meta.verbose_name_plural), "Users")

    def test_string_representation(self):
        user = UserModelFactory.build(favorites__skip=True)
        self.assertEqual(str(user), "{0} ({1})".format(user.full_name, user.email))

    def test_user_with_address(self):
        user = UserModel(
            email="timo@mancelot.app",
            full_name="Timo Halbesma",
            address="Straatnaam 42",
            zip_code="1337 XD",
            country="NL",
        )
        self.assertEqual(user.email, "timo@mancelot.app")
        self.assertEqual(user.full_name, "Timo Halbesma")
        self.assertEqual(user.address, "Straatnaam 42")
        self.assertEqual(user.country, "NL")

    def test_send_email_to_user(self):
        # user = UserModel(
        #     email="timo@mancelot.app",
        #     full_name="Timo Halbesma",
        # )
        # user.email_user(subject, message, from_email=settings.DEFAULT_FROM_EMAIL)
        pass
