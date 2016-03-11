from rest_framework import serializers

from api.models import Sighting, Picture


class SightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sighting


class PictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = ('file',)
