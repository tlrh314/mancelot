from rest_framework import serializers

from catalogue.models import Brand
from catalogue.models import Store
from catalogue.models import Category
from catalogue.models import Product


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ("name",)


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ("name",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ("name",)
