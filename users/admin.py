from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, TelegramUser, TelegramUserToken


@admin.register(CustomUser)
class AdminCustomUser(UserAdmin):
    fieldsets = (
        (
            None,
            {"fields": ("username", "password", "group", "email")},
        ),
        (
            "Advanced options",
            {
                "fields": (
                    "is_staff",
                    "groups",
                    "verified",
                    "is_active",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "group",
                    "email",
                ),
            },
        ),
    )
    list_display = [
        "id",
        "username",
        "group",
        "email",
        "verified",
        "is_staff",
        "is_active",
    ]
    search_fields = ["username", "group", "email"]
    list_display_links = ["username"]


@admin.register(TelegramUser)
class AdminTelegramUser(admin.ModelAdmin):
    list_display = ["id", "telegram_id", "username", "type_chat"]
    list_filter = ["type_chat"]


@admin.register(TelegramUserToken)
class AdminTelegramUserToken(admin.ModelAdmin):
    list_display = ["id", "token", "telegram_user"]
