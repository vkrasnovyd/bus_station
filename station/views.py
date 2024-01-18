from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView

from station.models import Bus
from station.serializers import BusSerializer


class BusListView(APIView):
    def get(self, request):
        buses = Bus.objects.all()
        serializer = BusSerializer(buses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BusDetailView(APIView):
    def get_object(self, pk):
        return generics.get_object_or_404(Bus, id=pk)

    def get(self, request, pk):
        bus = self.get_object(pk)
        serializer = BusSerializer(bus)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        bus = self.get_object(pk)
        serializer = BusSerializer(bus, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        bus = self.get_object(pk)
        serializer = BusSerializer(bus, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        bus = self.get_object(pk)
        bus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
