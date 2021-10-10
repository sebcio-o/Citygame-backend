from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import (
    CityViewSet,
    EventViewSet,
    QuestTypeViewSet,
    QuestViewSet,
    ReportViewSet,
    QuestsByTypeView,
)

router = SimpleRouter()
router.register(r"city", CityViewSet, basename="city")
router.register(r"event", EventViewSet, basename="event")
router.register(r"quest/type", QuestTypeViewSet, basename="quest-type")
router.register(r"quest", QuestViewSet, basename="quest")
router.register(r"report", ReportViewSet, basename="report")
urlpatterns = [
    path("questBYTYPE/<quest_type_id>/", QuestsByTypeView.as_view()),
] + router.urls
