from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

from filebrowser.sites import site
from rest_framework import routers

from catalogue.urls import router as catalogue_router


handler404 = "catalogue.views.handler404"
handler500 = "catalogue.views.handler500"

router = routers.DefaultRouter(False)
router.registry.extend(catalogue_router.registry)

urlpatterns = [
    path("admin/filebrowser/", site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("admin/", admin.site.urls),
    path("admin/password_reset/", auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",),
    path(r"admin/", include("django.contrib.auth.urls")),

    # path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("", RedirectView.as_view(url="index.html"), name="index"),
    path("", include("accounts.urls")),
    path("api/v1/", include(router.urls)),
    path("api/v1/auth/", include("rest_framework.urls")),
    path("privacy/", TemplateView.as_view(template_name="privacy_policy.html"), name="privacy_policy"),
]
