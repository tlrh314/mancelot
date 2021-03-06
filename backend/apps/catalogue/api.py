from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import (
    filters,
    generics,
    viewsets,
    pagination,
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
    Product,
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
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certificate.objects.order_by("name")
    serializer_class = CertificateSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Category.objects.filter(active=True)
        .prefetch_related("subcategories")
        .order_by("name")
        .distinct()
    )
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = ["section"]


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Subcategory.objects.filter(active=True)
        .select_related("category")
        .order_by("name")
        .distinct()
    )
    serializer_class = SubcategorySerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = ["category__section"]


class PaymentOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentOption.objects.order_by("id")
    serializer_class = PaymentOptionSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Store.objects.filter(active=True)
        .prefetch_related("payment_options")
        .order_by("id")
        .distinct()
    )
    serializer_class = StoreSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = [
        "payment_options",
    ]


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Brand.objects.filter(active=True)
        .order_by("id")
        .prefetch_related(
            "labels",
            "certificates",
        )
        .distinct()
    )

    serializer_class = BrandSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = ["labels", "certificates"]


class SizeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Size.objects.order_by("id")
    serializer_class = SizeSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Color.objects.order_by("id")
    serializer_class = ColorSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.order_by("id")
    serializer_class = MaterialSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Product.objects.filter(
            active=True,
            brand__active=True,
            store__active=True,
            categories__active=True,
            subcategories__active=True,
        )
        .order_by("id")
        .select_related(
            "brand",
        )
        .prefetch_related(
            "categories",
            "subcategories",
            "sizes",
            "colors",  # "materials",
            "brand__labels",
            "brand__certificates",
        )
        .distinct()
    )
    permission_classes = [
        permissions.IsAuthenticated,
    ]  # 1 query to usermodel
    filter_backends = [
        DjangoFilterBackend,
    ]
    filter_fields = [
        "categories__section",
        "categories",
        "subcategories",
        "brand",
        "brand__labels",
        "brand__certificates",
        "store",
        "colors",
        "sizes",  # "materials",
    ]
    pagination.PageNumberPagination.max_page_size = 1000
    pagination.PageNumberPagination.page_size_query_param = "page_size"

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        if self.action == "retrieve":
            return ProductRetrieveSerializer
        return super().get_serializer_class()  # create/destroy/update

    @method_decorator(cache_page(15 * 60))  # 15 minutes
    def list(self, request, format=None):
        return super().list(request, format=format)
