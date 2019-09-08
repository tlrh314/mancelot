from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotAuthenticated
# from mollie.api.client import Client as MollieClient

from accounts.models import UserModel
from accounts.serializers import UserModelSerializer
from accounts.permissions import IsAdminUserOrSelf


class UserModelViewSet(ModelViewSet):
    queryset = UserModel.objects.order_by("pk")
    serializer_class = UserModelSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "create":
            permission_classes = [AllowAny]
        elif self.action == "retrieve" or self.action == "update" or self.action == "partial_update":
            permission_classes = [IsAdminUserOrSelf]
        elif self.action == "list" or self.action == "destroy":
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_object(self):
        if self.kwargs["pk"] == "me":
            if self.request.user.is_authenticated:
                return self.request.user
            else:
                raise NotAuthenticated
        else:
            if not self.request.user.is_authenticated:
                raise NotAuthenticated
            if self.request.user.is_staff:
                # returns 404 if DoesNotExist, so would leak which pks exist
                # if we don't check for e.g. is_staff
                return super().get_object()
            user = UserModel.objects.filter(pk=self.kwargs["pk"]).first()
            if self.request.user == user:
                return user
            else:
                raise PermissionDenied
