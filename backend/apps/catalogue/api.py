from rest_framework import filters
from rest_framework import generics
from rest_framework import viewsets
# from django_filters.rest_framework import DjangoFilterBackend

from catalogue.models import Store
from catalogue.models import Brand
from catalogue.models import Category
from catalogue.models import Product
from catalogue.serializers import StoreSerializer
from catalogue.serializers import BrandSerializer
from catalogue.serializers import CategorySerializer
from catalogue.serializers import ProductSerializer


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
