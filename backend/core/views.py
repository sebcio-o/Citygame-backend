from django.db.models.query import QuerySet
from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from .serializers import (
    CitiesPaginationSerializer,
    CitySerializer,
    EventSerializer,
    EventsPaginationSerializer,
    QuestSerializer,
    QuestTypeSerializer,
    CreateQuestRequestBodySerializer,
)
from .models import City, Event, Quest, QuestType
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point
from rest_framework.pagination import LimitOffsetPagination


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = LimitOffsetPagination
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CitiesPaginationSerializer
        return CitySerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == "list":
            return EventsPaginationSerializer
        return EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        if city := self.request.query_params.get("city") and self.action == "list":
            return queryset.objects.filter(city=city)
        return queryset

    @extend_schema(
        parameters=[OpenApiParameter("city", OpenApiTypes.INT, OpenApiParameter.QUERY)]
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class QuestViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    pagination_class = LimitOffsetPagination
    serializer_class = QuestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Quest.objects.filter(user=self.request.user)
        if type_ := self.request.query_params.get("type") and self.action == "list":
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
        if event := self.request.query_params.get("event") and self.action == "list":
            return queryset.objects.filter(event=event)
        return queryset

    @extend_schema(
        parameters=[OpenApiParameter("event", OpenApiTypes.INT, OpenApiParameter.QUERY)]
    )
    def list(self, request):
        return super().list(self, request)