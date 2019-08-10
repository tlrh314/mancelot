from rest_framework import serializers
from django_countries.serializer_fields import CountryField

from accounts.models import UserModel


class UserModelSerializer(serializers.ModelSerializer):
    # id = IntegerField(label=_("id"), read_only=True)
    country = CountryField()

    class Meta:
        model = UserModel
        fields = (
            "email", "full_name",
            "address", "zip_code", "country",
            "balance", "monthly_top_up", "payment_preference"
        )

    def create(self, validated_data):
        return UserModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("email", instance.email)
        instance.style = validated_data.get("full_name", instance.full_name)

        instance.style = validated_data.get("address", instance.address)
        instance.style = validated_data.get("zip_code", instance.zip_code)
        instance.style = validated_data.get("country", instance.country)

        instance.style = validated_data.get("balance", instance.balance)
        instance.style = validated_data.get("monthly_top_up", instance.monthly_top_up)
        instance.style = validated_data.get("payment_preference", instance.payment_preference)

        instance.save()
        return instance
