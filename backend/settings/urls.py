from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from filebrowser.sites import site

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from accounts import api as accounts_api
from catalogue import api as catalogue_api

# handler404 = "catalogue.views.handler404"
handler500 = "catalogue.views.handler500"


router = routers.DefaultRouter()
router.register("catalogue/brand", catalogue_api.BrandViewSet)
router.register("catalogue/store", catalogue_api.StoreViewSet)
router.register("catalogue/Product", catalogue_api.ProductViewSet)


urlpatterns = [
    path("admin/filebrowser/", site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("admin/", admin.site.urls),
    path("admin/password_reset/", auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",),
    path(r"admin/", include("django.contrib.auth.urls")),

    path("api/v1/auth/", include("rest_framework.urls")),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/v1/users", accounts_api.UserModelCreateView.as_view(), name="create"),
    path("api/v1/users/me", accounts_api.UserModelDetailsView.as_view(), name="users"),
    path("api/v1/", include(router.urls)),

    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("accounts/", include("accounts.urls")),
    path("privacy/", TemplateView.as_view(template_name="privacy_policy.html"), name="privacy_policy"),
]
