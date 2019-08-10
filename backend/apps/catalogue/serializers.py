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

    def subcategories(self):
        self.subcategories.all()


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "category")


class PaymentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "logo")


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = (
            "id", "name", "slug", "info", "url", "logo", "payment_options",
        )


class BrandSerializer(serializers.HyperlinkedModelSerializer):
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


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "info", "extra_info", "url", "cece_id",
            "price", "from_price" "main_image", "extra_images", "brand", "store",
            "categories", "subcategories", "materials", "sizes", "colors",
        )
