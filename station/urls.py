from django.urls import path, include

from rest_framework import routers

from station.views import BusViewSet

router = routers.DefaultRouter()
router.register("buses", BusViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "station"
