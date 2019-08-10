from rest_framework import serializers

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


class CeceLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CeceLabel
        fields = ("name", "slug", "info")


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ("id", "name", "slug", "info")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "section", "subcategories")


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ("id", "name", "slug", "category")


class PaymentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOption
        fields = ("id", "name", "slug", "logo")


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = (
            "id", "name", "slug", "info", "url", "logo", "payment_options",
        )


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id", "name", "slug", "info", "url", "logo",
            "labels", "certificates"
        )


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ("id", "name", "slug")


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ("id", "name", "slug")


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ("id", "name", "slug", "info")


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "info", "extra_info", "url", "cece_id",
            "price", "price_currency", "from_price", "from_price_currency",
            "main_image", "extra_images", "brand", "store",
            "categories", "categories_api", "subcategories", "materials",
            "sizes", "colors",
        )
    def categories_api(self):
        return serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="category-list")
