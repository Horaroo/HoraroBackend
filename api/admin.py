from django.contrib import admin

from .models import Day, Event, Schedule, Type, Week


@admin.register(Schedule)
class AdminSchedule(admin.ModelAdmin):
    list_display = ["group", "week", "day", "subject", "number_pair"]
    search_fields = ["group", "week", "day"]


@admin.register(Day)
class AdminDay(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Week)
class AdminWeek(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Type)
class AdminType(admin.ModelAdmin):
    pass


@admin.register(Event)
class AdminEvent(admin.ModelAdmin):
    list_display = ["title", "created_at"]
