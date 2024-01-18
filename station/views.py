from rest_framework import mixins, viewsets

from station.models import Bus
from station.serializers import BusSerializer


class BusViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
