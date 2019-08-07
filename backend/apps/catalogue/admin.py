from django.contrib import admin
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
    Material,
    Product
)


class RelatedDropdownFilter(RelatedFieldListFilter):
    """ https://github.com/mrts/django-admin-list-filter-dropdown/ """
    template = "catalogue/dropdown_filter.html"


@admin.register(CeceLabel)
class CeceLabelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "info")
    ordering = ("name",)
    readonly_fields = ("slug", "date_created", "date_updated", "last_updated_by",)
    form = FixTinyMCEHasTooWideUIForm

    fieldsets = (
        (None, {"fields": ("name", "info")}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "info")
    ordering = ("name",)
    readonly_fields = ("slug", "date_created", "date_updated", "last_updated_by",)
    form = FixTinyMCEHasTooWideUIForm

    fieldsets = (
        (None, {"fields": ("name", "info")}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


class SubcategoryAdminInline(admin.StackedInline):
    model = Subcategory
    fields = ("name",)
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "section")
    list_filter = ("section",)
    search_fields = ("name",)
    ordering = ("section", "name",)
    readonly_fields = ("slug", "date_created", "date_updated", "last_updated_by",)
    inlines = (SubcategoryAdminInline,)

    fieldsets = (
        (None, {"fields": ("name", "section")}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(PaymentOption)
class PaymentOption(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("slug", "date_created", "date_updated", "last_updated_by",)

    fieldsets = (
        (None, {"fields": ("name", "logo")}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = (
        ("payment_options", RelatedDropdownFilter),
    )
    search_fields = ("name", "info")
    ordering = ("name",)
    readonly_fields = ("slug",  "date_created", "date_updated", "last_updated_by",)
    filter_horizontal = ("payment_options",)
    form = FixTinyMCEHasTooWideUIForm

    fieldsets = (
        (None, {"fields": ("name", "info", "url", "logo", "payment_options")}),
        (_("Contactgegevens (administratief)"), {"fields": ("address", "zip_code", "city", "country")}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = (
        ("labels", RelatedDropdownFilter),
        ("certificates", RelatedDropdownFilter),
    )
    search_fields = ("name", "info")
    ordering = ("name",)
    readonly_fields = ("slug", "date_created", "date_updated", "last_updated_by",)
    filter_horizontal = ("labels", "certificates")
    form = FixTinyMCEHasTooWideUIForm

    fieldsets = (
        (None, {"fields": ("name", "info", "url", "logo")}),
        (_("Duurzaamheidscriteria"), {"fields": ("labels", "certificates")}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("date_created",)
    readonly_fields = ("slug", "date_created", "date_updated", "last_updated_by",)

    fieldsets = (
        (None, {"fields": ("name",)}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name",)
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

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


# TODO: check once ProductFactory has support for from_price
class ProductIsOnSaleFilter(admin.SimpleListFilter):
    title = _("Uitverkoop")
    parameter_name = "sale"

    def lookups(self, request, model_admin):
        return ((False, _("Regulier")),
                (True, _("Uitverkoop")))

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
        "name", "cece_id", "date_updated", "section", "first_category",
        "brand", "store"
    )
    list_filter = (
        ("category", RelatedDropdownFilter),
        ("brand", RelatedDropdownFilter),
        ("store", RelatedDropdownFilter),
        ("material", RelatedDropdownFilter),
        ("size", RelatedDropdownFilter),
        ProductIsOnSaleFilter,
    )
    search_fields = ("name", "info", "extra_info",)
    ordering = ("name",)
    readonly_fields = ("slug", "date_created", "date_updated", "last_updated_by",)
    filter_horizontal = ("category", "subcategory", "material", "size")
    form = FixTinyMCEHasTooWideUIForm

    fieldsets = (
        (None, {"fields": (
            "name", "cece_id", "url", "price", "from_price",
            "main_image", "extra_images",
            "info", "extra_info",
            "brand", "store", "category",
            "color", "size", "material",
            )
        }),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("cece_api_url", "slug", "date_created", "date_updated", "last_updated_by")
        }),
    )

    def section(self, obj):
        if obj.category.count() > 0:
            return obj.category.first().section
        else:
            return "ERROR"
    section.short_description = _("Section1")

    def first_category(self, obj):
        if obj.category.count() > 0:
            return obj.category.first()
        else:
            return "ERROR"
    first_category.short_description = _("Category1")

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()

    def history_view(self, request, object_id, extra_context=None):
        """ Hack the history view such that it renders html """
        s = super(UserModelAdmin, self).history_view(request, object_id, extra_context=None)
        action_list = s.context_data["action_list"]
        for log_entry in action_list:
            try:
                log_entry.change_message = format_html(log_entry.change_message)
            except KeyError:
                pass
        return s
