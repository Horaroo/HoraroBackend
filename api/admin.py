from django.contrib import admin
from .models import UserProfile, Schedules, BlockUser, NumberWeek


@admin.register(UserProfile)
class AdminUserProfile(admin.ModelAdmin):
    list_display = ('username', 'group', 'telegram_id')
    search_fields = ('username', 'group')


@admin.register(Schedules)
class AdminSchedules(admin.ModelAdmin):
    list_display = ('group', )
    search_fields = ('group', )


@admin.register(BlockUser)
class AdminBlocUser(admin.ModelAdmin):
    list_display = ('username', 'group')
    search_fields = ('username', 'group')


@admin.register(NumberWeek)
class AdminNumberWeek(admin.ModelAdmin):
    pass

