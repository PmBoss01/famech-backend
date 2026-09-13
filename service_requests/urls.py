from rest_framework.routers import DefaultRouter

from service_requests.views import JobViewSet, RequestViewSet

app_name = "service_requests"

router = DefaultRouter()
router.register("requests", RequestViewSet, basename="request")
router.register("jobs", JobViewSet, basename="job")

urlpatterns = router.urls
