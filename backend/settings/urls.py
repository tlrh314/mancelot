from django.urls import path
from django.urls import re_path
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.conf.urls import include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test

from filebrowser.sites import site
from rest_framework import routers

from catalogue.urls import router as catalogue_router


@user_passes_test(lambda u: u.is_staff and u.is_superuser)
def flower_view(request, path):
    '''passes the request back up to nginx for internal routing'''
    import logging; logger = logging.getLogger("console")
    logger.error("The function argument is {0}".format(path))
    response = HttpResponse()
    path = request.get_full_path()
    logger.error("The bloody path was: {0}".format(path))
    path = path.replace("flower", "flower-internal", 1)
    logger.error("The bloody path is: {0}".format(path))
    response["X-Accel-Redirect"] = path
    return response


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
    path("admin/", include("django.contrib.auth.urls")),
    path("admin/silk/", include("silk.urls", namespace="silk")),
    re_path(r"^flower/(?P<path>.*)$", flower_view),

    # path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("", RedirectView.as_view(url="index.html"), name="index"),
    path("", include("accounts.urls")),
    path("api/v1/", include(router.urls)),
    path("api/v1/auth/", include("rest_framework.urls")),
    path("privacy/", TemplateView.as_view(template_name="privacy_policy.html"), name="privacy_policy"),
]
