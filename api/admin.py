from django.contrib import admin
from .models import UserProfile, Schedules, BlockUser, NumberWeek


@admin.register(UserProfile)
class AdminUserProfile(admin.ModelAdmin):
    fields = ('username', 'group', 'telegram_id')
    search_fields = ('username', 'group')


@admin.register(Schedules)
class AdminSchedules(admin.ModelAdmin):
    fields = ('group', )
    search_fields = ('group', )


@admin.register(BlockUser)
class AdminBlocUser(admin.ModelAdmin):
    fields = ('username', 'group')
    search_fields = ('username', 'group')


@admin.register(NumberWeek)
class AdminNumberWeek(admin.ModelAdmin):
    pass

