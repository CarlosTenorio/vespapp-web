from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from api.models import Sighting
from api.serializers import SightingSerializer


class SightingListCreateView(ListCreateAPIView):
    serializer_class = SightingSerializer

    def get_queryset(self):
        return Sighting.objects.order_by('-created_at')


class SightingRetrieveUpdateView(RetrieveUpdateAPIView):

    serializer_class = SightingListCreateView
    lookup_url_kwarg = 'sighting_id'
    lookup_field = 'id'