from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Sighting, Picture, Location, Question, Answer, SightingInfo
from api.serializers import SightingSerializer, PictureSerializer, LocationSerializer, ProvinceSerializer, QuestionSerializer, \
    AnswerSerializer, MyQuestionSerializer, SightingInfoSerializer
from api.models import Sighting, UserComment, ExpertComment
from api.serializers import SightingSerializer, UserCommentSerializer, ExpertCommentSerializer


# Sightings list
class SightingListCreateView(ListCreateAPIView):
    serializer_class = SightingSerializer

    def get_queryset(self):
        return Sighting.objects.order_by('-created_at')


# One sighting
class SightingRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = SightingSerializer
    queryset = Sighting.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'sighting_id'


# Pictures of sighting
class SightingPictureCreateView(ListCreateAPIView):
    serializer_class = PictureSerializer

    def get_queryset(self):
        sighting_id = self.kwargs.get('sighting_id')
        return Picture.objects.filter(sighting__pk=sighting_id)

    def create(self, request, *args, **kwargs):
        request.data['sighting'] = kwargs.get('sighting_id')
        return super().create(request, *args, **kwargs)


# Questions&Answers
class SightingQuestionsListView(ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return self

    def get(self, request, *args, **kwargs):
        sighting_id = self.kwargs.get('sighting_id')
        sighting = Sighting.objects.get(pk=sighting_id)

        questions = Question.objects.filter(sighting_type=sighting.type)

        for question in questions:
            question_answers = sighting.answers.filter(question_id=question.id)
            question.answers = question_answers

        question_serializer = MyQuestionSerializer(questions, many=True)

        return Response(question_serializer.data)


# Locations list
class LocationsList(ListAPIView):
    serializer_class = LocationSerializer

    def get_queryset(self):
        return Location.objects.all()


# Provinces list
class ProvincesList(ListAPIView):
    serializer_class = ProvinceSerializer

    def get_queryset(self):
        return Provinces.objects.all()


# Info list
class SightingInfoList(ListAPIView):
    serializer_class = SightingInfoSerializer

    def get_queryset(self):
        return SightingInfo.objects.all()











# Comments
class SightingUserCommentsListView(ListCreateAPIView):
    serializer_class = UserCommentSerializer

    def get_queryset(self):
        sighting_id = self.kwargs.get('sighting_id')
        return UserComment.objects.filter(sighting__pk=sighting_id)

    def create(self, request, *args, **kwargs):
        request.data['sighting'] = kwargs.get('sighting_id')
        return super().create(request, *args, **kwargs)


# Expert comments
class SightingExpertCommentsListView(ListCreateAPIView):
    serializer_class = ExpertCommentSerializer

    def get_queryset(self):
        sighting_id = self.kwargs.get('sighting_id')
        return ExpertComment.objects.filter(sighting__pk=sighting_id)

    def create(self, request, *args, **kwargs):
        request.data['sighting'] = kwargs.get('sighting_id')
        return super().create(request, *args, **kwargs)














class SightingAnswerRetrieveUpdate(RetrieveUpdateAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        sighting_id = self.kwargs.get('sighting_id')
        sighting_type = Sighting.objects.filter(id=sighting_id)
        questions = Question.objects.filter(type=sighting_type)
        answers = Answer.objects.filter(question__in=questions)


class SightingQuestionsCreateView(ListCreateAPIView):
    serializer_class = UserCommentSerializer

    def get_queryset(self):
        sighting_id = self.kwargs.get('sighting_id')
        return ExpertComment.objects.filter(sighting__pk=sighting_id)

    def create(self, request, *args, **kwargs):
        request.data['sighting'] = kwargs.get('sighting_id')
        return super().create(request, *args, **kwargs)


class SightingUserCommentView(ListCreateAPIView):
    serializer_class = UserCommentSerializer

    def get_queryset(self):
        sighting_id = self.kwargs['sighting_id']
        comments = UserComment.objects.filter(sighting=sighting_id)
        return comments

    def post(self, sighting_id):
        #sighting_id = self.kwargs['sighting_id']

        if not Sighting.objects.exists(id=sighting_id):
            return None

        sighting = Sighting.objects.get(id=sighting_id)

        new_comment = UserComment(
                body='pruebahehehe',
                sighting=sighting,
        )

        new_comment.save()

        return new_comment
