from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import (
    filters,
    generics,
    viewsets,
    permissions,
)
from rest_framework.response import Response
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
    ProductListSerializer,
    ProductRetrieveSerializer,
)


class CeceLabelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CeceLabel.objects.order_by("name")
    serializer_class = CeceLabelSerializer
    permission_classes = [permissions.IsAuthenticated,]


class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certificate.objects.order_by("name")
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated,]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related("subcategories").order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = ["section"]


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subcategory.objects.select_related("category").order_by("name")
    serializer_class = SubcategorySerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = ["category__section"]


class PaymentOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentOption.objects.order_by("id")
    serializer_class = PaymentOptionSerializer
    permission_classes = [permissions.IsAuthenticated,]


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.prefetch_related("payment_options").order_by("id")
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = ["payment_options",]


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.order_by("id").prefetch_related(
        "labels",
        "certificates",
    )

    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = ["labels", "certificates"]


class SizeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Size.objects.order_by("id")
    serializer_class = SizeSerializer
    permission_classes = [permissions.IsAuthenticated,]


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Color.objects.order_by("id")
    serializer_class = SizeSerializer
    permission_classes = [permissions.IsAuthenticated,]


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.order_by("id")
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated,]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.order_by("id").select_related(
        "brand",
    ).prefetch_related(
        "categories", "subcategories", "sizes", "colors",  # "materials",
        "brand__labels", "brand__certificates"
    )
    permission_classes = [permissions.IsAuthenticated,]  # 1 query to usermodel
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = [
        "categories__section", "categories", "subcategories",
        "brand", "brand__labels", "brand__certificates", "store",
        "colors", "sizes",  # "materials",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        if self.action == "retrieve":
            return ProductRetrieveSerializer
        return super().get_serializer_class()  # create/destroy/update

    @method_decorator(cache_page(15 * 60))  # 15 minutes
    def list(self, request, format=None):
        return super().list(request, format=format)
