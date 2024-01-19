from rest_framework import serializers

from station.models import Bus


class BusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bus
        fields = "__all__"
        read_only_fields = ("id",)
