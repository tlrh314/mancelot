from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from djmoney.models.fields import MoneyField
from django_countries.fields import CountryField

from accounts.managers import AccountManager


class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email"), max_length=254, unique=True)
    full_name = models.CharField(
        _("full name"), max_length=150, null=True, help_text=_("First and last name")
    )
    address = models.CharField(
        _("address"),
        max_length=128,
        null=True,
        blank=True,
        help_text=_("Streetname and housenumber"),
    )
    zip_code = models.CharField(_("zip code"), max_length=10, null=True, blank=True)
    city = models.CharField(_("city"), max_length=42, null=True, blank=True)
    country = CountryField(_("country"), default="NL", null=True, blank=True)

    # Support for monthly subscriptions
    PAYMENT_OPTIONS = (
        (0, _("Bank Transfer")),
        (1, _("Ideal")),
        (2, _("Paypal")),
    )
    iban = models.CharField(_("iban"), max_length=42, null=True, blank=True)
    balance = MoneyField(
        _("balance"),
        null=True,
        blank=True,
        max_digits=19,
        decimal_places=4,
        default_currency="EUR",
    )
    monthly_top_up = MoneyField(
        _("monthly top up"),
        null=True,
        blank=True,
        max_digits=19,
        decimal_places=4,
        default_currency="EUR",
    )
    payment_preference = models.PositiveSmallIntegerField(
        _("payment preference"),
        null=True,
        blank=True,
        choices=PAYMENT_OPTIONS,
        default=None,
    )

    # Django permission fields
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        _("staff"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_superuser = models.BooleanField(_("superuser"), default=False)

    # Bookkeeping of changes
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date Laatst Gewijzigd"), auto_now=True)
    last_updated_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="has_changed_accounts",
        verbose_name=_("last updated by"),
    )

    objects = AccountManager()

    USERNAME_FIELD = "email"  # email login rather than arbitrary username
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return "{0} ({1})".format(self.full_name, self.email)

    def email_user(
        self,
        subject,
        text_content,
        html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        **kwargs
    ):

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[self.email],
            bcc=settings.ADMIN_BCC,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def send_welcome_email(self):
        subject = "Welkom bij Mancelot"
        text_content = "Welkom bij Mancelot!"
        html_content = render_to_string("accounts/welcome.html")
        self.email_user(subject, text_content, html_content)
