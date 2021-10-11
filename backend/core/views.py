from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets, views
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from .serializers import (
    CitySerializer,
    EventSerializer,
    QuestSerializer,
    QuestTypeSerializer,
    CreateRequestBodyQuestSerializer,
)
from .models import City, Event, Quest, QuestType
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    @extend_schema(
        parameters=[OpenApiParameter("city", OpenApiTypes.INT, OpenApiParameter.QUERY)]
    )
    def list(self, request, *args, **kwargs):
        if city := request.query_params.get("city"):
            queryset = Event.objects.filter(city=city)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        return super().list(self, request, *args, **kwargs)


class QuestViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    serializer_class = QuestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Quest.objects.filter(user=user)
        if type_ := self.request.query_params.get("type"):
            parent = QuestType.objects.filter(id=type_).first()
            queryset = queryset.filter(parent=parent)
        return queryset

    @extend_schema(
        parameters=[OpenApiParameter("type", OpenApiTypes.INT, OpenApiParameter.QUERY)]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(request=CreateRequestBodyQuestSerializer)
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
    serializer_class = QuestTypeSerializer
    queryset = QuestType.objects.all()

    @extend_schema(
        parameters=[OpenApiParameter("event", OpenApiTypes.INT, OpenApiParameter.QUERY)]
    )
    def list(self, request):
        if event := request.query_params.get("event"):
            queryset = QuestType.objects.filter(event=event)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        return super().list(self, request)