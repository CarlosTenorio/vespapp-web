from rest_framework import serializers

from api.models import Sighting


class SightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sighting
