from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from api.serializers import SightingSerializer


class SightingListCreateView(ListCreateAPIView):
    serializer_class = SightingSerializer

    def get_queryset(self):
        return


class SightingRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = SightingListCreateView
