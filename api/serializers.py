from rest_framework import serializers

from api.models import Sighting, Picture


class SightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sighting


class PictureSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['sighting'] = 1
        return super().create(validated_data)

    class Meta:
        model = Picture
        fields = ('file',)
