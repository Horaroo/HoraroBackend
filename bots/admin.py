from django.contrib import admin
from .models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "category", "created_at"]
    list_filter = ["category"]


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
