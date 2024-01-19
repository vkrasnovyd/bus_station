from rest_framework import viewsets

from station.models import Bus, Trip
from station.serializers import (
    BusSerializer,
    TripSerializer,
    TripListSerializer
)


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TripListSerializer

        return TripSerializer
