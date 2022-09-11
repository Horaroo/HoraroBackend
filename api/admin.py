from django.contrib import admin
from .models import NumberWeek, Schedule, Day, Week, Type, Event


@admin.register(Schedule)
class AdminSchedule(admin.ModelAdmin):
    list_display = ['group', 'week', 'day', 'subject', 'number_pair']
    search_fields = ['group', 'week', 'day']


@admin.register(Day)
class AdminDay(admin.ModelAdmin):
    pass


@admin.register(Week)
class AdminWeek(admin.ModelAdmin):
    pass


@admin.register(Type)
class AdminType(admin.ModelAdmin):
    pass


# @admin.register(BlockUser)
# class AdminBlocUser(admin.ModelAdmin):
#     list_display = ('username', 'telegram_id')
#     search_fields = ('username', )


@admin.register(NumberWeek)
class AdminNumberWeek(admin.ModelAdmin):
    pass


@admin.register(Event)
class AdminEvent(admin.ModelAdmin):
    pass
