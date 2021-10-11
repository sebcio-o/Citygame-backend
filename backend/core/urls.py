from rest_framework.routers import SimpleRouter
from .views import (
    CityViewSet,
    EventViewSet,
    QuestTypeViewSet,
    QuestViewSet,
)

router = SimpleRouter()
router.register(r"cities", CityViewSet, basename="city")
router.register(r"events", EventViewSet, basename="event")
router.register(r"quests/types", QuestTypeViewSet, basename="quest-type")
router.register(r"quests", QuestViewSet, basename="quest")
urlpatterns = router.urls
