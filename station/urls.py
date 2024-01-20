from rest_framework import routers

from station.views import BusViewSet, TripViewSet, FacilityViewSet

router = routers.DefaultRouter()
router.register("buses", BusViewSet, basename="bus")
router.register("trips", TripViewSet, basename="trip")
router.register("facilities", FacilityViewSet, basename="facility")

urlpatterns = router.urls

app_name = "station"
