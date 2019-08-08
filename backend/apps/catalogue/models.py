from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField
from tinymce.models import HTMLField
from filebrowser.fields import FileBrowseField
from django_countries.fields import CountryField


class CeceLabel(models.Model):
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), blank=True, max_length=255, unique=True)
    info = HTMLField(_("info"), null=True, blank=True)

    # Fields for bookkeeping of database updates
    cece_api_url = models.URLField(_("cece_api_url"), null=True, blank=True)
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)
    last_updated_by = models.ForeignKey("accounts.UserModel",
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name="has_changed_cecelabel")

    class Meta:
        verbose_name = _("Label")
        verbose_name_plural = _("Labels")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     # TODO: reverse the REST endpoint?
    #     return reverse("catalogue:todo", args=[self.pk])


class Certificate(models.Model):
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), blank=True, max_length=255, unique=True)
    info = HTMLField(_("info"), null=True, blank=True)
    #  url = models.URLField(_("url"))  # TODO: add url of certificate instance website?

    # Fields for bookkeeping of database updates
    cece_api_url = models.URLField(_("cece_api_url"), null=True, blank=True)
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)
    last_updated_by = models.ForeignKey("accounts.UserModel",
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name="has_changed_certificate")

    class Meta:
        verbose_name = _("Certificate")
        verbose_name_plural = _("Certificates")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     # TODO: reverse the REST endpoint?
    #     return reverse("catalogue:todo", args=[self.pk])


class Category(models.Model):
    SECTIONS = (
       (0, _("Men")),
       (1, _("Women")),
       (2, _("Kids")),
    )

    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), blank=True, max_length=255, unique=True)
    section = models.PositiveSmallIntegerField(
        "sectie", choices=SECTIONS, default=0
    )

    # Fields for bookkeeping of database updates
    cece_api_url = models.URLField(_("cece_api_url"), null=True, blank=True)
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)
    last_updated_by = models.ForeignKey("accounts.UserModel",
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name="has_changed_category")

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     # TODO: reverse the REST endpoint?
    #     return reverse("catalogue:todo", args=[self.pk])


class Subcategory(models.Model):
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), blank=True, max_length=255, unique=True)
    category = models.ForeignKey(Category,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )

    # Fields for bookkeeping of database updates
    cece_api_url = models.URLField(_("cece_api_url"), null=True, blank=True)
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)
    last_updated_by = models.ForeignKey("accounts.UserModel",
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="has_changed_subcategory")

    class Meta:
        verbose_name = _("Subcategory")
        verbose_name_plural = _("Subcategories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     # TODO: reverse the REST endpoint?
    #     return reverse("catalogue:todo", args=[self.pk])


class PaymentOption(models.Model):
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), blank=True, max_length=255, unique=True)
    logo = FileBrowseField(_("logo"), default="/static/img/test/test_logo.png",
        max_length=200, directory="{0}/img/logos/payment".format(settings.STATIC_ROOT),
        extensions=[".jpg", ".jpeg", ".gif", ".png"],
    )

    # Fields for bookkeeping of database updates
    cece_api_url = models.URLField(_("cece_api_url"), null=True, blank=True)
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)
    last_updated_by = models.ForeignKey("accounts.UserModel",
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="has_changed_paymentoption")

    class Meta:
        verbose_name = _("PaymentOption")
        verbose_name_plural = _("PaymentOptions")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     # TODO: reverse the REST endpoint?
    #     return reverse("catalogue:todo", args=[self.pk])


class Store(models.Model):
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), blank=True, max_length=255, unique=True)
    info = HTMLField(_("info"), null=True, blank=True)
    url = models.URLField(_("url"))
    logo =  FileBrowseField(_("logo"), default="/static/img/test/test_logo.png",
        max_length=200, directory="{0}img/logos/stores".format(settings.STATIC_ROOT),
        extensions=[".jpg", ".jpeg", ".gif", ".png"],
    )
    payment_options = models.ManyToManyField(PaymentOption, related_name="stores")

    # Administrative address, e.g. headquarters
    address = models.CharField(_("address"), max_length=128, null=True, blank=True)
    zip_code = models.CharField(_("zip code"), max_length=10, null=True, blank=True)
    city = models.CharField(_("city"), max_length=42, null=True, blank=True)
    country = CountryField(_("country"), default="NL", null=True, blank=True)

    # Fields for bookkeeping of database updates
    cece_api_url = models.URLField(_("cece_api_url"), null=True, blank=True)
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)
    last_updated_by = models.ForeignKey("accounts.UserModel",
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="has_changed_store")

    class Meta:
        verbose_name = _("Store")
        verbose_name_plural = _("Stores")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     # TODO: reverse the REST endpoint?
    #     return reverse("catalogue:todo", args=[self.pk])


class Brand(models.Model):
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), blank=True, max_length=255, unique=True)
    info = HTMLField(_("info"), null=True, blank=True)
    url = models.URLField(_("url"), null=True, blank=True)
    logo =  FileBrowseField(_("logo"), default="/static/img/test/test_logo.png",
        max_length=200, directory="{0}/img/logos/brands".format(settings.STATIC_ROOT),
        extensions=[".jpg", ".jpeg", ".gif", ".png"],
    )

    # Sustainability information, gleaned from Cece API
    labels = models.ManyToManyField(CeceLabel, blank=True, related_name="brands")
    certificates = models.ManyToManyField(Certificate, blank=True, related_name="brands")

    # Fields for bookkeeping of database updates
    cece_api_url = models.URLField(_("cece_api_url"), null=True, blank=True)
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)
    last_updated_by = models.ForeignKey("accounts.UserModel",
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="has_changed_brand")

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brand")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     # TODO: reverse the REST endpoint?
    #     return reverse("catalogue:todo", args=[self.pk])


class Size(models.Model):
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), blank=True, max_length=255, unique=True)

    # Fields for bookkeeping of database updates
    cece_api_url = models.URLField(_("cece_api_url"), null=True, blank=True)
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)
    last_updated_by = models.ForeignKey("accounts.UserModel",
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="has_changed_size")

    class Meta:
        verbose_name = _("Size")
        verbose_name_plural = _("Sizes")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), blank=True, max_length=255, unique=True)
    info = HTMLField(_("info"), null=True, blank=True)

    # Fields for bookkeeping of database updates
    cece_api_url = models.URLField(_("cece_api_url"), null=True, blank=True)
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)
    last_updated_by = models.ForeignKey("accounts.UserModel",
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="has_changed_material")

    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Material")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), blank=True, max_length=255, unique=True)
    info = HTMLField(_("info"), null=True, blank=True)
    extra_info = HTMLField(_("extra info"), null=True, blank=True)
    url = models.URLField(_("url"))

    cece_id = models.CharField(_("cece product id"), null=True, blank=True, max_length=100)

    price = models.DecimalField(_("price"), max_digits=6, decimal_places=2)
    from_price = models.DecimalField(_("from price"), max_digits=6,
        decimal_places=2, null=True, blank=True,
        help_text=_("Product on sale if 'from price' is given.")
    )

    main_image = models.URLField(_("main image"), max_length=450)
    extra_images = JSONField(_("extra images"), blank=True)

    brand = models.ForeignKey(Brand,
        related_name="products",
        on_delete=models.CASCADE
    )
    store = models.ForeignKey(Store,
        related_name="products",
        on_delete=models.CASCADE
    )
    # TODO: handle deletion of the last Category from Product (delete Product?)
    categories = models.ManyToManyField(Category,
        related_name="products",
    )
    subcategories = models.ManyToManyField(Subcategory,
        related_name="products",
        blank=True,
    )
    materials = models.ManyToManyField(Material,
        related_name="products",
        blank=True
    )
    sizes = models.ManyToManyField(Size,
        related_name="products",
        blank=True
    )
    color = models.CharField(_("color"), null=True, blank=True, max_length=200)

    # Fields for bookkeeping of database updates
    cece_api_url = models.URLField(_("cece_api_url"), null=True, blank=True)
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)
    last_updated_by = models.ForeignKey("accounts.UserModel",
        on_delete=models.SET_NULL, blank=True, null=True,
        related_name="has_changed_product")

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     # TODO: reverse the REST endpoint?
    #     return reverse("catalogue:todo", args=[self.pk])
