from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets, views
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework.response import Response
from .serializers import (
    AllCitiesSerializer,
    AllEventsSerializer,
    AllQuestTypesSerializer,
    AllQuestsSerializer,
    CitySerializer,
    EventSerializer,
    QuestSerializer,
    QuestTypeSerializer,
    CreateRequestBodyQuestSerializer,
    ReportSerializer,
)
from .models import City, Event, Quest, QuestType, Report
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins
from rest_framework.decorators import permission_classes as f_permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.gis.geos import Point


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AllCitiesSerializer
        return CitySerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()

    @extend_schema(
        parameters=[OpenApiParameter("city", OpenApiTypes.INT, OpenApiParameter.QUERY)]
    )
    def list(self, request, *args, **kwargs):
        if city := request.query_params.get("city"):
            queryset = Event.objects.filter(city=city)
            serializer = AllEventsSerializer(queryset, many=True)
            return Response(serializer.data)
        return super().list(self, request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return AllEventsSerializer
        return EventSerializer


class QuestTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QuestType.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AllQuestTypesSerializer
        return QuestTypeSerializer

    @extend_schema(
        parameters=[OpenApiParameter("event", OpenApiTypes.INT, OpenApiParameter.QUERY)]
    )
    def list(self, request):
        if event := request.query_params.get("event"):
            queryset = QuestType.objects.filter(event=event)
            serializer = AllQuestTypesSerializer(queryset, many=True)
            return Response(serializer.data)
        return super().list(self, request)


class QuestViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Quest.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == "list":
            return AllQuestsSerializer
        return QuestSerializer

    @extend_schema(request=CreateRequestBodyQuestSerializer)
    def create(self, request, *args, **kwargs):

        parent = request.data.get("parent")
        geom = Point(*request.data.get("point"))

        try:
            quest_type = QuestType.objects.get(id=parent, polygon__intersects=geom)
        except QuestType.DoesNotExist:
            raise ParseError(detail="Quest type doesn't exists")

        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail="User not authenticated")

        q = Quest.objects.create(
            parent=quest_type,
            user=request.user,
            finish_date=request.data.get("finish_date"),
        )
        serializer = QuestSerializer(q)
        return Response(serializer.data)


class ReportViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = [IsAdminUser]

    @f_permission_classes([IsAuthenticated])
    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        return super().create(request, *args, **kwargs)


@f_permission_classes([IsAuthenticated])
class QuestsByTypeView(views.APIView):
    def get(self, request, quest_type_id):
        print(request.user.id)
        query_set = Quest.objects.filter(
            user=request.user.id, parent=int(quest_type_id)
        )
        serializer = QuestSerializer(query_set, many=True)
        return Response(serializer.data)