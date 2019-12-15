from rest_framework import validators
from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

from accounts.models import UserModel
from catalogue.serializers import SizeSerializer
from catalogue.serializers import ProductListSerializer


class UserModelSerializer(CountryFieldMixin, serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[validators.UniqueValidator(
            queryset=UserModel.objects.all().values_list("email", flat=True)
        )]
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        required=False,
        style={"input_type": "password", "placeholder": "Password"}
    )

    class Meta:
        model = UserModel
        fields = (
            "id", "email", "full_name", "password",
            "address", "zip_code", "country",
            "balance", "monthly_top_up", "payment_preference", "iban",
        )
        read_only_fields = ("balance",)

    def create(self, validated_data):
        try:
            password = validated_data.pop("password")
        except KeyError:
            raise serializers.ValidationError({"password": ["This field is required.",]})
        user = super(UserModelSerializer, self).create(validated_data)
        user.set_password(password)
        user.is_active=True
        user.save()
        user.send_welcome_email()
        return user

    def update(self, instance, validated_data):
        for field in validated_data:
            if field == "password":
                instance.set_password(validated_data.get(field))
            else:
                instance.__setattr__(field, validated_data.get(field))
        instance.save()
        return instance

    def partial_update(self, instance, validated_data):
        for field in validated_data:
            if field == "password":
                instance.set_password(validated_data.get(field))
            else:
                instance.__setattr__(field, validated_data.get(field))
        instance.save()
        return instance


class UserFavoriteProductListSerializer(serializers.Serializer):
    product = ProductListSerializer()
    size = SizeSerializer()
    quantity = serializers.IntegerField()


class UserFavoritePatchSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    # TODO: Optional for MancelotAlpha0-9, but mandatory in later versions
    size_id = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField()


class UserFavoriteDeleteSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    # TODO: Optional for MancelotAlpha0-9, but mandatory in later versions
    size_id = serializers.IntegerField(required=False)
