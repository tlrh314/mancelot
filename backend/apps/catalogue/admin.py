from django.urls import reverse
from django.contrib import admin
from django.db.models import Count, Sum
from django.utils.html import format_html
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.filters import RelatedFieldListFilter

from catalogue.forms import FixTinyMCEHasTooWideUIForm
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


class RelatedDropdownFilter(RelatedFieldListFilter):
    """ https://github.com/mrts/django-admin-list-filter-dropdown/ """
    template = "catalogue/dropdown_filter.html"


@admin.register(CeceLabel)
class CeceLabelAdmin(admin.ModelAdmin):
    list_display = ("name", "get_count",)
    search_fields = ("name", "info")
    ordering = ("name",)
    readonly_fields = ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by",)
    form = FixTinyMCEHasTooWideUIForm

    fieldsets = (
        (None, {"fields": ("name", "info")}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            count=Sum("brands__products")
        )

    def get_count(self, obj):
        return obj.count
    get_count.short_description = _("# Products")
    get_count.admin_order_field = "count"

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("name", "get_count")
    search_fields = ("name", "info")
    ordering = ("name",)
    readonly_fields = ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by",)
    form = FixTinyMCEHasTooWideUIForm

    fieldsets = (
        (None, {"fields": ("name", "info")}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            count=Sum("brands__products")
        )

    def get_count(self, obj):
        return obj.count
    get_count.short_description = _("# Products")
    get_count.admin_order_field = "count"

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "get_count", "get_category", "get_section")
    search_fields = ("name", "category")
    ordering = ("category__section", "category", "name",)
    readonly_fields = ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by",)

    fieldsets = (
        (None, {"fields": ("name", "category", )}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category").annotate(
            count=Count("products")
        )

    def get_count(self, obj):
        return obj.count
    get_count.short_description = _("# Products")
    get_count.admin_order_field = "count"

    def get_category(self, obj):
        return format_html(
            "<a href='{0}'>{1}</a>".format(reverse("admin:catalogue_category_change",
            args=[obj.category.pk]), obj.category.name)
        )
    get_category.short_description = _("Category")
    get_category.admin_order_field = "category__name"

    def get_section(self, obj):
        return obj.category.get_section_display()
    get_section.short_description = _("Section")

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


class SubcategoryAdminInline(admin.StackedInline):
    model = Subcategory
    fields = ("name",)
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "get_count", "section", "get_subcategories")
    list_filter = ("section",)
    search_fields = ("name",)
    ordering = ("section", "name",)
    readonly_fields = ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by",)
    inlines = (SubcategoryAdminInline,)

    fieldsets = (
        (None, {"fields": ("name", "section")}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            count=Count("products")
        )

    def get_count(self, obj):
        return obj.count
    get_count.short_description = _("# Products")
    get_count.admin_order_field = "count"

    def get_subcategories(self, obj):
        return format_html(
            "<br>".join("<a href='{0}'>{1}</a>".format(
                reverse("admin:catalogue_subcategory_change", args=[c.pk]), c.name)
                for c in obj.subcategories.iterator()
            )
        )
    get_subcategories.short_description = _("Subcategories")

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(PaymentOption)
class PaymentOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "show_logo",)
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by",)

    fieldsets = (
        (None, {"fields": ("name", "logo")}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def show_logo(self, obj):
        return format_html(
            "<img src='{0}' alt='{1}', height='42' width/>".format(obj.logo, obj.name)
        )
    show_logo.short_description = _("Logo")

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "get_count", "show_logo")
    list_filter = (
        ("payment_options", RelatedDropdownFilter),
    )
    search_fields = ("name", "info")
    ordering = ("name",)
    readonly_fields = ("cece_api_url", "slug",  "date_created", "date_updated", "last_updated_by",)
    filter_horizontal = ("payment_options",)
    form = FixTinyMCEHasTooWideUIForm

    fieldsets = (
        (None, {"fields": ("name", "info", "url", "logo", "payment_options")}),
        (_("Address (administrative)"), {"fields": ("address", "zip_code", "city", "country")}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            count=Count("products")
        )

    def get_count(self, obj):
        return obj.count
    get_count.short_description = _("# Products")
    get_count.admin_order_field = "count"

    def show_logo(self, obj):
        return format_html(
            "<img src='{0}' alt='{1}', height='42' width/>".format(obj.logo, obj.name)
        )
    show_logo.short_description = _("Logo")

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "get_count", "get_certificates", "get_labels")
    list_filter = (
        ("labels", RelatedDropdownFilter),
        ("certificates", RelatedDropdownFilter),
    )
    search_fields = ("name", "info")
    ordering = ("name",)
    readonly_fields = ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by",)
    filter_horizontal = ("labels", "certificates")
    form = FixTinyMCEHasTooWideUIForm

    fieldsets = (
        (None, {"fields": ("name", "info", "url", "logo")}),
        (_("Sustainability criteria"), {"fields": ("labels", "certificates")}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            "labels", "certificates",
        ).annotate(
            count=Count("products"),
        )

    def get_count(self, obj):
        return obj.count
    get_count.short_description = _("# Products")
    get_count.admin_order_field = "count"

    def get_labels(self, obj):
        return format_html(
            "<br>".join("<a href='{0}'>{1}</a>".format(
                reverse("admin:catalogue_cecelabel_change", args=[c.pk]), c.name)
                for c in obj.labels.all()
            )
        )
    get_labels.short_description = _("Labels")

    def get_certificates(self, obj):
        return format_html(
            "<br>".join("<a href='{0}'>{1}</a>".format(
                reverse("admin:catalogue_certificate_change", args=[c.pk]), c.name)
                for c in obj.certificates.all()
            )
        )
    get_certificates.short_description = _("Certificates")

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("name", "get_count",)
    search_fields = ("name",)
    ordering = ("date_created",)
    readonly_fields = ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by",)

    fieldsets = (
        (None, {"fields": ("name",)}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            count=Count("products")
        )

    def get_count(self, obj):
        return obj.count
    get_count.short_description = _("# Products")
    get_count.admin_order_field = "count"

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "get_count",)
    search_fields = ("name",)
    ordering = ("date_created",)
    readonly_fields = ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by",)

    fieldsets = (
        (None, {"fields": ("name",)}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            count=Count("products")
        )

    def get_count(self, obj):
        return obj.count
    get_count.short_description = _("# Products")
    get_count.admin_order_field = "count"

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "get_count")
    search_fields = ("name", "info")
    ordering = ("name",)
    readonly_fields = ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by",)
    form = FixTinyMCEHasTooWideUIForm

    fieldsets = (
        (None, {"fields": ("name", "info")}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            count=Count("products")
        )

    def get_count(self, obj):
        return obj.count
    get_count.short_description = _("# Products")
    get_count.admin_order_field = "count"

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


# TODO: check once ProductFactory has support for from_price
class ProductIsOnSaleFilter(admin.SimpleListFilter):
    title = _("Sale")
    parameter_name = "sale"

    def lookups(self, request, model_admin):
        return ((False, _("Regular")),
                (True, _("Sale")))

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(from_price__isnull=False)
        elif self.value() == "False":
            return queryset.filter(from_price__isnull=True)
        else:
            return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_brand", "get_store",
        "get_categories", "get_sections",
        "cece_id",
        "date_created", "date_updated",
    )
    list_filter = (
        ("categories", RelatedDropdownFilter),
        ("brand", RelatedDropdownFilter),
        ("store", RelatedDropdownFilter),
        ("materials", RelatedDropdownFilter),
        ("sizes", RelatedDropdownFilter),
        ("colors", RelatedDropdownFilter),
        ProductIsOnSaleFilter,
    )
    search_fields = ("name", "info", "extra_info",)
    ordering = ("name",)
    readonly_fields = ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by",)
    filter_horizontal = ("categories", "subcategories", "materials", "sizes", "colors")
    form = FixTinyMCEHasTooWideUIForm

    fieldsets = (
        (None, {"fields": (
            "name", "cece_id", "url", "price", "from_price",
            "main_image", "extra_images",
            "info", "extra_info",
            "brand", "store", "categories",
            "colors", "sizes", "materials",
            )
        }),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "brand", "store",
        ).prefetch_related(
            "categories", "subcategories", "colors", "sizes",
        )

    def get_brand(self, obj):
        return format_html(
            "<a href='{0}'>{1}</a>".format(reverse("admin:catalogue_brand_change",
            args=[obj.brand.pk]), obj.brand.name)
        )
    get_brand.short_description = _("Brand")
    get_brand.admin_order_field = "brand"

    def get_store(self, obj):
        return format_html(
            "<a href='{0}'>{1}</a>".format(reverse("admin:catalogue_store_change",
            args=[obj.store.pk]), obj.store.name)
        )
    get_store.short_description = _("Store")
    get_store.admin_order_field = "store"

    def get_labels(self, obj):
        return format_html(
            "<br>".join("<a href='{0}'>{1}</a>".format(
                reverse("admin:catalogue_label_change", args=[c.pk]), c.name)
                for c in obj.brand.labels.iterator()
            )
        )
    get_labels.short_description = _("Labels")
    get_labels.admin_order_field = "brand__labels__name"

    def get_certificates(self, obj):
        return format_html(
            "<br>".join("<a href='{0}'>{1}</a>".format(
                reverse("admin:catalogue_certificates_change", args=[c.pk]), c.name)
                # .iterator here seemed 300 ms faster than .all while the
                # number of queries did not increase. Curious.
                for c in obj.brand.certificates.iterator()
            )
        )
    get_certificates.short_description = _("Certificates")
    get_certificates.admin_order_field = "brand__certificates__name"

    def get_categories(self, obj):
        return format_html(
            "<br>".join("<a href='{0}'>{1}</a>".format(
                reverse("admin:catalogue_category_change", args=[c.pk]), c.name)
                # for some reason iterator starts querying the db, whereas
                # all does not (b/c prefetched). Curious.
                for c in obj.categories.all()
            )
        )
    get_categories.short_description = _("Categories")
    get_categories.admin_order_field = "categories__name"

    def get_sections(self, obj):
        return format_html("<br>".join( c.get_section_display() for c in obj.categories.all() ))
    get_sections.short_description = _("Sections")
    get_sections.admin_order_field = "categories__section"

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

    def history_view(self, request, object_id, extra_context=None):
        """ Hack the history view such that it renders html """
        s = super().history_view(request, object_id, extra_context=None)
        action_list = s.context_data["action_list"]
        for log_entry in action_list:
            try:
                log_entry.change_message = format_html(log_entry.change_message)
            except KeyError:
                pass
        return s
