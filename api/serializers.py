from rest_framework import serializers
from api.models import Sighting, Picture, UserComment, ExpertComment

class SightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sighting


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComment


class ExpertCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertComment


class PictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = ('file',)
