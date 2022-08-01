from django.contrib import admin
from .models import UserProfile, Schedules, BlockUser, NumberWeek


@admin.register(UserProfile)
class AdminUserProfile(admin.ModelAdmin):
    list_display = ('user', 'group', 'telegram_id')
    search_fields = ('user', 'group')


@admin.register(Schedules)
class AdminSchedules(admin.ModelAdmin):
    search_fields = ('group', )


@admin.register(BlockUser)
class AdminBlocUser(admin.ModelAdmin):
    list_display = ('username', 'telegram_id')
    search_fields = ('username', )


@admin.register(NumberWeek)
class AdminNumberWeek(admin.ModelAdmin):
    pass

