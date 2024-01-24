from rest_framework import routers

from station.views import (
    BusViewSet,
    TripViewSet,
    FacilityViewSet,
    OrderViewSet,
)

router = routers.DefaultRouter()
router.register("buses", BusViewSet, basename="bus")
router.register("trips", TripViewSet, basename="trip")
router.register("facilities", FacilityViewSet, basename="facility")
router.register("orders", OrderViewSet, basename="order")

urlpatterns = router.urls

app_name = "station"
