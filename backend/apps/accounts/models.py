from django.db import models
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.encoding import python_2_unicode_compatible

from django_countries.fields import CountryField

from accounts.managers import AccountManager


@python_2_unicode_compatible
class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email Address"), max_length=254, unique=True)
    full_name = models.CharField(_("Volledige naam"), max_length=150, null=True)
    address = models.CharField(_("Straatnaam huisnummer"), max_length=128, null=True, blank=True)
    zip_code = models.CharField(_("Postcode"), max_length=10, null=True, blank=True)
    city = models.CharField(_("Stad"), max_length=42, null=True, blank=True)
    country = CountryField(_("Land"), default="NL", null=True, blank=True)

    # Support
    favorites = models.ManyToManyField("catalogue.Product", verbose_name=_("favorieten"),
        related_name="saved_by_users", blank=True)

    # Django permission fields
    is_active = models.BooleanField(_("Active"), default=False,
        help_text="Designates whether this user should be treated as "
        "active. Unselect this instead of deleting accounts.")
    is_staff = models.BooleanField(_("Staff"), default=False,
        help_text="Designates whether the user can log into this admin site.")
    is_superuser = models.BooleanField(_("Superuser"), default=False)

    # Bookkeeping of changes
    date_created = models.DateTimeField(_("Datum Aangemaakt"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Datum Laatst Gewijzigd"), auto_now=True)
    last_updated_by = models.ForeignKey("self",
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="has_changed_accounts")

    objects = AccountManager()

    USERNAME_FIELD = "email"  # email login rather than arbitrary username
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = _("Gebruiker")
        verbose_name_plural = _("Gebruikers")

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
