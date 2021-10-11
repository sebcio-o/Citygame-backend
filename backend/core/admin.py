from django.contrib import admin
from .models import Event, City, QuestType, Quest

admin.site.register([Event, City, QuestType, Quest])
