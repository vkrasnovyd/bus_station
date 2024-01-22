from django.db.models import Count, F
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from station.models import Bus, Trip, Facility, Order
from station.permissions import IsAdminOrIFAuthenticatedReadOnly
from station.serializers import (
    BusSerializer,
    BusListSerializer,
    BusDetailSerializer,
    TripSerializer,
    TripListSerializer,
    TripDetailSerializer,
    FacilitySerializer,
    OrderSerializer,
    OrderListSerializer,
)


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIFAuthenticatedReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        return [int(param_id) for param_id in qs.split(",")]

    def get_queryset(self):
        queryset = self.queryset

        facilities = self.request.query_params.get("facilities")
        if facilities:
            facilities_ids = self._params_to_ints(facilities)
            queryset = (
                queryset.filter(facilities__id__in=facilities_ids).distinct()
            )

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIFAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("bus").annotate(
                tickets_available=F("bus__num_seats") - Count("tickets")
            )

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIFAuthenticatedReadOnly,)


class OrderPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIFAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == "list":
            queryset = queryset.prefetch_related("tickets__trip__bus")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
