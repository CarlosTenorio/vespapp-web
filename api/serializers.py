from rest_framework import serializers
from api.models import Sighting, Picture, UserComment, ExpertComment, Question, Answer, Location, Province, SightingInfo


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture


class SightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sighting


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComment


class ExpertCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertComment


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer


class QuestionSerializer(serializers.ModelSerializer):
    available_answers = AnswerSerializer(source='default_answer', many=True)

    class Meta:
        model = Question


class MyQuestionSerializer(serializers.ModelSerializer):
    available_answers = AnswerSerializer(source='default_answer', many=True)
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question


class SightingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SightingInfo
