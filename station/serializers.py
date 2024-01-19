from rest_framework import serializers

from station.models import Bus, Trip


class BusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bus
        fields = ("id", "info", "num_seats", "is_mini")
        read_only_fields = ("id",)


class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ("id", "source", "destination", "departure", "bus")


class TripListSerializer(TripSerializer):
    bus = BusSerializer(many=False, read_only=True)
