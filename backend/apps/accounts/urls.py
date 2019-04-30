from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from django.views.generic import TemplateView

app_name = "accounts"
urlpatterns = [
    path("profile/", TemplateView.as_view(template_name="accounts/profile.html"), name="profile"),
]
