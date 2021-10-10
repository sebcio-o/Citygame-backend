from django.contrib import admin
from .models import Event, City, QuestType, Quest, Report

admin.site.register([Event, City, QuestType, Quest, Report])
