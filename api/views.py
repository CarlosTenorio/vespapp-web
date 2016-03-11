from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from api.models import Sighting, Picture
from api.serializers import SightingSerializer, PictureSerializer


class SightingListCreateView(ListCreateAPIView):
    serializer_class = SightingSerializer

    def get_queryset(self):
        return Sighting.objects.order_by('-created_at')


class SightingRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = SightingSerializer
    queryset = Sighting.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'sighting_id'


class SightingPictureCreateView(ListCreateAPIView):
    serializer_class = PictureSerializer

    def get_queryset(self):
        sighting_id = self.kwargs.get('sighting_id')
        return Picture.objects.filter(sighting__pk=sighting_id)
    
    def create(self, request, *args, **kwargs):
        request.data['sighting'] = self.kwargs.get('sighting')
        return super().create(request, *args, **kwargs)

