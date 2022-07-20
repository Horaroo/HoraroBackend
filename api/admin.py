from django.contrib import admin
from .models import UserProfile, Schedules, BlockUser, NumberWeek


@admin.register(UserProfile)
class AdminUserProfile(admin.ModelAdmin):
    pass


@admin.register(Schedules)
class AdminSchedules(admin.ModelAdmin):
    pass


@admin.register(BlockUser)
class AdminBlocUser(admin.ModelAdmin):
    pass


@admin.register(NumberWeek)
class AdminNumberWeek(admin.ModelAdmin):
    pass

