from django.http import JsonResponse

from station.models import Bus
from station.serializers import BusSerializer


def bus_list(request):
    if request.method == "GET":
        buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
