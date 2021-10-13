from django.contrib.gis.geos import Point

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .mixins import ListDetailSerializerSplitMixin
from .models import City, Event, Quest, QuestType, Reward
from .serializers import (
    CitiesPaginationSerializer,
    CitySerializer,
    CreateQuestRequestBodySerializer,
    EventSerializer,
    EventsPaginationSerializer,
    QuestSerializer,
    QuestTypeSerializer,
    RewardSerializer,
)


class CityViewSet(viewsets.ReadOnlyModelViewSet, ListDetailSerializerSplitMixin):
    pagination_class = LimitOffsetPagination
    queryset = City.objects.all()
    detail_serializer_class = CitySerializer
    list_serializer_class = CitiesPaginationSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet, ListDetailSerializerSplitMixin):
    pagination_class = LimitOffsetPagination
    detail_serializer_class = EventSerializer
    list_serializer_class = EventsPaginationSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        if (city := self.request.query_params.get("city")) and self.action == "list":
            return queryset.objects.filter(city=city)
        return queryset

    @extend_schema(
        parameters=[OpenApiParameter("city", OpenApiTypes.INT, OpenApiParameter.QUERY)]
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class RewardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticated]

    def get_rewards_from_event(self, event_id):
        rewards = []
        quests = Quest.objects.filter(user=self.request.user)
        quest_types_ids = [i.id for i in QuestType.objects.filter(event=event_id)]
        for i in quest_types_ids:
            if quests.objects.filter(parent=i).first():
                rewards.append(Reward.objects.filter(event=event_id).first())
        return rewards

    def get_queryset(self):
        if event_id := self.request.query_params.get("event"):
            return self.get_rewards_from_event(event_id)

        rewards = []
        for event in Event.objects.all():
            rewards += self.get_rewards_from_event(event.id)
        return rewards

    @extend_schema(
        parameters=[OpenApiParameter("event", OpenApiTypes.INT, OpenApiParameter.QUERY)]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class QuestViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    pagination_class = LimitOffsetPagination
    serializer_class = QuestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Quest.objects.filter(user=self.request.user)
        if (type_ := self.request.query_params.get("type")) and self.action == "list":
            parent = QuestType.objects.filter(id=type_).first()
            return queryset.filter(parent=parent)
        return queryset

    @extend_schema(
        parameters=[OpenApiParameter("type", OpenApiTypes.INT, OpenApiParameter.QUERY)]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(request=CreateQuestRequestBodySerializer)
    def create(self, request, *args, **kwargs):
        parent = request.data.get("parent")
        geom = Point(*request.data.get("point"))
        try:
            quest_type = QuestType.objects.get(id=parent, polygon__intersects=geom)
        except QuestType.DoesNotExist:
            raise ParseError(detail="Quest type doesn't exists")

        quest = Quest.objects.create(
            parent=quest_type,
            user=request.user,
            finish_date=request.data.get("finish_date"),
        )
        serializer = self.serializer_class(quest)
        return Response(serializer.data)


class QuestTypeViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = LimitOffsetPagination
    serializer_class = QuestTypeSerializer

    def get_queryset(self):
        queryset = QuestType.objects.all()
        if (event := self.request.query_params.get("event")) and self.action == "list":
            return queryset.objects.filter(event=event)
        return queryset

    @extend_schema(
        parameters=[OpenApiParameter("event", OpenApiTypes.INT, OpenApiParameter.QUERY)]
    )
    def list(self, request):
        return super().list(self, request)
