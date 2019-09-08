from django.urls import path
from django.views.generic import TemplateView

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from accounts.api import UserModelViewSet

router = routers.SimpleRouter()
router.register("users", UserModelViewSet)

app_name = "accounts"
urlpatterns = [
    path("api/v1/auth/jwtoken/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/jwtoken/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/auth/jwtoken/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("accounts/profile/", TemplateView.as_view(template_name="accounts/profile.html"), name="profile"),
]
