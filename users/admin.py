from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TelegramUser, GroupUserTelegram


@admin.register(CustomUser)
class AdminCustomUser(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'group', 'email')
        }),
        ('Advanced options', {
            'fields': ('is_staff', 'groups', 'verified', 'is_active'),
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
    list_display = ['username', 'group', 'email', 'verified', 'is_staff', 'is_active']
    search_fields = ['username', 'group', 'email']
    list_display_links = ['username']


@admin.register(TelegramUser)
class AdminTelegramUser(admin.ModelAdmin):
    list_display = ['telegram_id', 'username', 'is_moder']


@admin.register(GroupUserTelegram)
class AdminGroupUser(admin.ModelAdmin):
    pass
