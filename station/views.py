from rest_framework import viewsets

from station.models import Bus, Trip, Facility, Order
from station.serializers import (
    BusSerializer,
    BusListSerializer,
    BusDetailSerializer,
    TripSerializer,
    TripListSerializer,
    TripDetailSerializer,
    FacilitySerializer,
    OrderSerializer,
)


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ("list", "retrieve"):
            return queryset.prefetch_related("facilities")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BusListSerializer

        if self.action == "retrieve":
            return BusDetailSerializer

        return self.serializer_class


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ("list", "retrieve"):
            return queryset.select_related("bus")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return TripListSerializer

        if self.action == "retrieve":
            return TripDetailSerializer

        return TripSerializer


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
