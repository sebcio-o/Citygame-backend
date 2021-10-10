from rest_framework.routers import SimpleRouter

from .views import (
    CityViewSet,
    EventViewSet,
    QuestTypeViewSet,
    QuestViewSet,
    ReportViewSet,
)

router = SimpleRouter()
router.register(r"city", CityViewSet, basename="city")
router.register(r"event", EventViewSet, basename="event")
router.register(r"quest/type", QuestTypeViewSet, basename="quest-type")
router.register(r"quest", QuestViewSet, basename="quest")
router.register(r"report", ReportViewSet, basename="report")
urlpatterns = router.urls