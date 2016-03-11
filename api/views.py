from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from api.models import Sighting, Picture
from api.serializers import SightingSerializer, PictureSerializer


class SightingListCreateView(ListCreateAPIView):
    serializer_class = SightingSerializer

    def get_queryset(self):
        return Sighting.objects.order_by('-created_at')


class SightingRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = SightingListCreateView
    lookup_url_kwarg = 'sighting_id'
    lookup_field = 'id'
    queryset = Sighting.objects.all()


class SightingPictureCreateView(ListCreateAPIView):
    serializer_class = PictureSerializer

    def get_queryset(self):
        sighting_id = self.kwargs.get('sighting_id')
        return Picture.objects.filter(sighting__pk=sighting_id)
    
    def create(self, request, *args, **kwargs):
        import ipdb
        ipdb.set_trace()
        sighting_id = self.kwargs.get('sighting_id')
        request.data['sighting'] = Sighting.objects.get(pk=sighting_id)
        return super(SightingPictureCreateView, self).create(request, *args, **kwargs)