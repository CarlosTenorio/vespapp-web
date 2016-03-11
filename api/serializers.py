from rest_framework import serializers

from api.models import Sighting, Picture


class SightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sighting


class PictureSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        request = self.context.get('request')
        print(request)
        sighting = Sighting.objects.get(pk=1)
        validated_data['sighting'] = sighting
        return super().create(validated_data)

    class Meta:
        model = Picture
        fields = ('file',)
