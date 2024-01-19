from rest_framework import viewsets

from station.models import Bus, Trip
from station.serializers import (
    BusSerializer,
    BusListSerializer,
    TripSerializer,
    TripListSerializer,
)


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            return queryset.prefetch_related("facilities")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BusListSerializer

        return self.serializer_class


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            return queryset.select_related("bus")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return TripListSerializer

        return TripSerializer
