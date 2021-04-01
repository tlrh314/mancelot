from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotAuthenticated

# from mollie.api.client import Client as MollieClient

from catalogue.models import (
    Size,
    Product,
    FavoriteProduct,
)
from accounts.models import UserModel
from accounts.serializers import UserModelSerializer
from accounts.permissions import IsAdminUserOrSelf
from accounts.serializers import (
    UserFavoriteProductListSerializer,
    UserFavoritePatchSerializer,
    UserFavoriteDeleteSerializer,
)


class UserModelViewSet(ModelViewSet):
    queryset = UserModel.objects.order_by("pk")

    def get_serializer_class(self):
        if self.action == "favorites":
            return UserFavoriteProductListSerializer
        return UserModelSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "create":
            permission_classes = [AllowAny]
        elif (
            self.action == "retrieve"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            permission_classes = [IsAdminUserOrSelf]
        elif self.action == "list" or self.action == "destroy":
            permission_classes = [IsAdminUser]
        elif self.action == "favorites":
            permission_classes = [IsAdminUserOrSelf]
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

    @action(methods=["get", "patch", "delete"], detail=True)
    def favorites(self, request, pk=None):
        user = self.get_object()

        if self.request.method == "GET":
            return Response(
                UserFavoriteProductListSerializer(
                    [fav for fav in user.favorites.all()], many=True
                ).data
            )

        if self.request.method == "PATCH":
            serializer = UserFavoritePatchSerializer(data=request.data)
            if serializer.is_valid():
                product_id = serializer.data["product_id"]
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    return Response(
                        {"status": "Product does not exist"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # TODO: Optional for MancelotAlpha0-9, but mandatory in later versions
                size_id = serializer.data.get("size_id", None)
                try:
                    size = Size.objects.get(id=size_id)
                except Size.DoesNotExist:
                    return Response(
                        {"status": "Size does not exist"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Check that the desired Size is available for the particular
                # Product instance. Note, however, that this could change any
                # time the data are updated from Cece API...
                if size not in product.sizes.all():
                    status_str = (
                        "Size not available for this Product. Choose id from: {0}"
                    )
                    status_str = status_str.format([p.id for p in product.sizes.all()])
                    return Response(
                        {"status": status_str}, status=status.HTTP_400_BAD_REQUEST
                    )

                quantity = serializer.data["quantity"]
                fav = FavoriteProduct.objects.filter(
                    product=product, user=user, size=size
                ).first()
                if fav:
                    if quantity == 0:
                        fav.delete()
                        return Response(
                            {"status": "Favorite deleted (b/c quantity is 0)"},
                            status=status.HTTP_200_OK,
                        )
                    else:
                        was = fav.quantity
                        fav.quantity = quantity
                        fav.save()
                        return Response(
                            {
                                "status": "Favorite quantity updated from {0} to {1}".format(
                                    was, quantity
                                )
                            },
                            status=status.HTTP_200_OK,
                        )
                else:
                    fav = FavoriteProduct.objects.create(
                        product=product, user=user, quantity=quantity
                    )
                    user.favorites.add(fav)
                    return Response(
                        {"status": "Favorite added"}, status=status.HTTP_200_OK
                    )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if self.request.method == "DELETE":
            serializer = UserFavoriteDeleteSerializer(data=request.data)
            if serializer.is_valid():
                product_id = serializer.data["product_id"]
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    return Response(
                        {"status": "Product does not exist"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # TODO: Optional for MancelotAlpha0-9, but mandatory in later versions
                size_id = serializer.data.get("size_id", None)
                try:
                    size = Size.objects.get(id=size_id)
                except Size.DoesNotExist:
                    return Response(
                        {"status": "Size does not exist"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                fav = FavoriteProduct.objects.filter(
                    product=product,
                    user=user,
                    size=size,
                ).first()
                if fav:
                    fav.delete()
                    return Response(
                        {"status": "Favorite deleted"}, status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"status": "Favorite does not exist"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Fallback, but if method not in methods on action, then 405 already returned
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
