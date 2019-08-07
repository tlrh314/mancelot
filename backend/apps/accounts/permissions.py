from rest_framework.permissions import BasePermission

from account.models import UserModel


class IsUserModelInstace(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, UserModel):
            return obj == request.user
        return obj == request.user
