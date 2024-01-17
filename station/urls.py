from django.urls import path

from station.views import bus_list

urlpatterns = [
    path("buses/", bus_list, name="bus-list"),
]

app_name = "station"
