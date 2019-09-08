from rest_framework.permissions import BasePermission

from accounts.models import UserModel


class IsAdminUserOrSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser
