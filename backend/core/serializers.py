from django.contrib.gis.db.models import fields
from rest_framework import request, serializers
from .models import City, Event, Quest, QuestType, Report


class AllCitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class AllEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class AllQuestTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestType
        fields = ["id"]


class QuestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestType
        fields = "__all__"


class AllQuestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = ["id"]


class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = "__all__"


class CreateRequestBodyQuestSerializer(serializers.ModelSerializer):
    point = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Quest
        fields = ["id", "parent", "finish_date", "point"]


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "title", "description", "category", "user"]
        extra_kwargs = {"user": {"read_only": True}}
