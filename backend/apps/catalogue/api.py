from rest_framework import filters
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
# from django_filters.rest_framework import DjangoFilterBackend

from catalogue.models import (
    CeceLabel,
    Certificate,
    Category,
    Subcategory,
    PaymentOption,
    Store,
    Brand,
    Size,
    Color,
    Material,
    Product
)
from catalogue.serializers import (
    CeceLabelSerializer,
    CertificateSerializer,
    CategorySerializer,
    SubcategorySerializer,
    PaymentOptionSerializer,
    StoreSerializer,
    BrandSerializer,
    SizeSerializer,
    ColorSerializer,
    MaterialSerializer,
    ProductSerializer
)


class CeceLabelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CeceLabel.objects.order_by("name")
    serializer_class = CeceLabelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]


class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certificate.objects.order_by("name")
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subcategory.objects.order_by("name")
    serializer_class = SubcategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]


class PaymentOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentOption.objects.order_by("name")
    serializer_class = PaymentOptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.order_by("name")
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.order_by("name")
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]


class SizeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Size.objects.order_by("name")
    serializer_class = SizeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Color.objects.order_by("name")
    serializer_class = SizeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.order_by("name")
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.order_by("name")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
