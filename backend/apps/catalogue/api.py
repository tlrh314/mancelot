from rest_framework import filters
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

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
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filter_fields = ["name"]
    ordering_fields = ["name",]
    search_fields = ["name",]


class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certificate.objects.order_by("name")
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filter_fields = ["name"]
    ordering_fields = ["name",]
    search_fields = ["name",]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filter_fields = ["name"]
    ordering_fields = ["name",]
    search_fields = ["name",]


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subcategory.objects.order_by("name")
    serializer_class = SubcategorySerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filter_fields = ["name"]
    ordering_fields = ["name",]
    search_fields = ["name",]


class PaymentOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentOption.objects.order_by("name")
    serializer_class = PaymentOptionSerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filter_fields = ["name"]
    ordering_fields = ["name",]
    search_fields = ["name",]


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.order_by("name")
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filter_fields = ["name"]
    ordering_fields = ["name",]
    search_fields = ["name",]


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.order_by("name").prefetch_related(
        "labels",
        "certificates",
    )

    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filter_fields = ["name"]
    ordering_fields = ["name",]
    search_fields = ["name",]


class SizeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Size.objects.order_by("name")
    serializer_class = SizeSerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filter_fields = ["name"]
    ordering_fields = ["name",]
    search_fields = ["name",]


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Color.objects.order_by("name")
    serializer_class = SizeSerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filter_fields = ["name"]
    ordering_fields = ["name",]
    search_fields = ["name",]


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.order_by("name")
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filter_fields = ["name"]
    ordering_fields = ["name",]
    search_fields = ["name",]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related(
        "brand", "store").prefetch_related(
        "categories", "subcategories", "colors", "sizes", "materials",
    ).all().order_by("name")
    # queryset = Product.objects.select_related().all().order_by("name")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filter_fields = [
        "name", "price", "from_price",
        "brand", "store", "categories", "subcategories",
    ]
    ordering_fields = ["name",]
    search_fields = ["name", "info", "extra_info",]
