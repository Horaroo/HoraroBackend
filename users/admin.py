from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Faculty, Group


@admin.register(CustomUser)
class AdminCustomUser(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'group', 'email')
        }),
        ('Advanced options', {
            'fields': ('is_staff', 'groups'),
        }),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": ("username", "password1", "password2", 'group', 'email'),
            },
        ),
    )
    list_display = ['username', 'group', 'email', 'is_staff']
    search_fields = ['username', 'group', 'email']


@admin.register(Faculty)
class AdminFaculty(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Group)
class AdminGroup(admin.ModelAdmin):
    list_display = ['name', 'faculty']
    search_fields = ['name', 'faculty']
