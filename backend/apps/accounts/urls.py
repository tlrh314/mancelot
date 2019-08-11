from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from django.views.generic import TemplateView

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    # Alternatively, could use sliding tokens
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)

from accounts.api import (
    UserModelCreateView,
    UserModelDetailsView
)


# TODO: add jwt views to router so they're visible in the browsable interface
# router = routers.SimpleRouter()
# router.register("auth/jwtoken", TokenObtainPairView)

app_name = "accounts"
urlpatterns = [
    path("api/v1/auth/jwtoken/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/jwtoken/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/auth/jwtoken/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/v1/users", UserModelCreateView.as_view(), name="create"),
    path("api/v1/users/me", UserModelDetailsView.as_view(), name="users"),

    path("accounts/profile/", TemplateView.as_view(template_name="accounts/profile.html"), name="profile"),
]
