from django.urls import path

from station.views import BusListView, BusDetailView

urlpatterns = [
    path("buses/", BusListView.as_view(), name="bus-list"),
    path("buses/<int:pk>/", BusDetailView.as_view(), name="bus-detail"),
]

app_name = "station"
