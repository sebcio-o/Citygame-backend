from django.contrib import admin

from .models import City, Event, Quest, QuestType, Reward

admin.site.register([Event, City, QuestType, Quest, Reward])
