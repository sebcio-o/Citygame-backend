from rest_framework import serializers

from .models import City, Event, Quest, QuestType, Reward


class CitiesPaginationSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class EventsPaginationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = "__all__"


class QuestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestType
        fields = "__all__"


class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = ["id", "parent", "finish_date"]


class CreateQuestRequestBodySerializer(serializers.ModelSerializer):
    point = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Quest
        fields = ["id", "parent", "finish_date", "point"]
