from rest_framework import serializers

from api.models import Sighting, Picture


class SightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sighting


class PictureSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        sighting_id = self.kwargs.get('sighting_id')
        sighting = Sighting.objects.get(pk=sighting_id)
        validated_data['sighting'] = sighting
        return super().create(validated_data)

    class Meta:
        model = Picture
        fields = ('file',)
