from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions
from ..fields import UUIDField
from ..models import Google_Authenticator

class DeleteGASerializer(serializers.Serializer):

    google_authenticator_id = UUIDField(required=True)

    def validate(self, attrs: dict) -> dict:

        google_authenticator_id = attrs.get('google_authenticator_id')

        try:
            google_authenticator = Google_Authenticator.objects.get(pk=google_authenticator_id, user=self.context['request'].user)
        except Google_Authenticator.DoesNotExist:
            msg = _("NO_PERMISSION_OR_NOT_EXIST")
            raise exceptions.ValidationError(msg)

        google_authenticator_count = Google_Authenticator.objects.filter(user=self.context['request'].user, active=True).count()



        attrs['google_authenticator'] = google_authenticator
        attrs['google_authenticator_count'] = google_authenticator_count

        return attrs