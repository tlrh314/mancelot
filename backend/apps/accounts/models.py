from django.db import models
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.encoding import python_2_unicode_compatible

from django_countries.fields import CountryField

from accounts.managers import UserModelManager


@python_2_unicode_compatible
class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email Address", max_length=254, unique=True)
    first_name = models.CharField("First Name", max_length=42)
    last_name = models.CharField("Last Name", max_length=42)
    full_name = models.CharField("Full Name", max_length=42, null=True)
    address = models.CharField("Address", max_length=128, null=True, blank=True)
    zip_code = models.CharField("Zip Code", max_length=10, null=True, blank=True)
    city = models.CharField("City", max_length=42, null=True, blank=True)
    country = CountryField("Country", default="NL", blank=True, null=True)

    is_active = models.BooleanField("Active", default=False,
        help_text="Designates whether this user should be treated as "
        "active. Unselect this instead of deleting accounts.")
    is_staff = models.BooleanField("Staff", default=False,
        help_text="Designates whether the user can log into this admin site.")
    is_superuser = models.BooleanField("Superuser", default=False)

    last_updated_by = models.ForeignKey("self",
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name="has_changed_accounts")
    date_created = models.DateTimeField("Date Created", auto_now_add=True)
    date_updated = models.DateTimeField("Date Last Changed", auto_now=True)

    objects = UserModelManager()

    USERNAME_FIELD = "email"  # email login rather than arbitrary username
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return "{0} ({1})".format(self.full_name, self.email)

    def email_user(self, subject, message, from_email=settings.DEFAULT_FROM_EMAIL, **kwargs):
        """ Sends an email to this User. Caution, from_email must contain domain
            name in production! """

        EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[self.email],
            bcc=settings.ADMIN_BCC,
        ).send(fail_silently=False)
