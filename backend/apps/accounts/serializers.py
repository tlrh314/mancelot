from rest_framework import serializers
from django_countries.serializer_fields import CountryField

from accounts.models import UserModel


class UserModelSerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = UserModel
        fields = ("email", "full_name", "address", "zip_code", "country")
        # read_only_fields = ("date_created", "date_modified")
