from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from station.models import Bus
from station.serializers import BusSerializer


@api_view(["GET"])
def bus_list(request):
    if request.method == "GET":
        buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
