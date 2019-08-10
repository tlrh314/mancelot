from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import ugettext_lazy as _


from accounts.models import UserModel


@admin.register(UserModel)
class UserModelAdmin(UserAdmin):
    list_display = (
        "email", "full_name", "is_active", "is_staff", "is_superuser", "date_created", "last_login",
    )
    list_filter = ("is_active", "is_staff", "is_superuser",)
    search_fields = ("email", "full_name")
    ordering = ("-date_created",)
    readonly_fields = ("last_login", "date_created", "last_updated_by",)
    filter_horizontal = ("groups", "user_permissions", "favorites",)
    actions = ("send_password_reset",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal information"), {"fields": (
            "full_name", "address", "zip_code", "city", "country",)
        }),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser",
            "groups", "user_permissions")}),
        (_("Content interaction"), {"fields": ("favorites",)}),
        (_("Subscription"), {"fields": ("balance", "monthly_top_up", "payment_preference")}),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("last_login", "date_created", "last_updated_by")
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2")}
        ),
    )

    def send_password_reset(self, request, queryset):
        for user in queryset:
            try:
                validate_email( user.email )
                form = PasswordResetForm(data={"email": user.email})
                form.is_valid()

                form.save(email_template_name="accounts/password_forced_reset_email.html",
                          extra_email_context={ "full_name": user.full_name })
                self.message_user(request, _("Succesfully sent password reset email."))
            except ValidationError:
                self.message_user(request, _("User does not have a valid email address"), level="error")
    send_password_reset.short_description = _("Send password reset link")

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

admin.site.unregister(Group)
