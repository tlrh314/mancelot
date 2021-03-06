from accounts.urls import router as accounts_router
from accounts.views import index
from catalogue.urls import router as catalogue_router
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from filebrowser.sites import site
from rest_framework import routers


@user_passes_test(lambda u: u.is_staff and u.is_superuser)
@csrf_exempt
def flower_view(request, path):
    """passes the request back up to nginx for internal routing"""
    response = HttpResponse()
    path = request.get_full_path()
    path = path.replace("flower", "flower-internal", 1)
    response["X-Accel-Redirect"] = path
    return response


handler404 = "catalogue.views.handler404"
handler500 = "catalogue.views.handler500"

router = routers.DefaultRouter(False)
router.registry.extend(accounts_router.registry)
router.registry.extend(catalogue_router.registry)

urlpatterns = [
    path("admin/filebrowser/", site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("admin/", admin.site.urls),
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path("admin/", include("django.contrib.auth.urls")),
    path("admin/silk/", include("silk.urls", namespace="silk")),
    re_path(r"^flower/(?P<path>.*)$", flower_view),
    path("", index, name="index"),
    path("", include("accounts.urls")),
    path("api/v1/", include(router.urls)),
    path("api/v1/auth/", include("rest_framework.urls")),
    path(
        "privacy/",
        TemplateView.as_view(template_name="privacy_policy.html"),
        name="privacy_policy",
    ),
]
