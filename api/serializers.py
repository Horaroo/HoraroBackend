from rest_framework import serializers

from api import services
from users.models import TelegramUser

from .models import *


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            "number_pair",
            "subject",
            "teacher",
            "audience",
            "week",
            "group",
            "type_pair",
            "day",
            "start_time",
            "end_time",
        )


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class TelegramUserSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source="token.group", read_only=True)

    class Meta:
        model = TelegramUser
        fields = [
            "telegram_id",
            "username",
            "is_moder",
            "token",
            "action",
            "token_name",
            "group",
        ]
        extra_kwargs = {"token": {"write_only": "True"}}

    token_name = serializers.SerializerMethodField()

    def get_token_name(self, instance):
        if instance.token:
            return instance.token.username

    def is_valid(self, raise_exception=False):
        data = self.initial_data.dict()
        if data.get("token"):
            data["token"] = CustomUser.objects.get(username=data["token"]).pk
            self.initial_data = data
        return super().is_valid()


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["title", "description", "picture", "cover", "is_main", "created_at"]


class ScheduleCopySerializer(serializers.ModelSerializer):
    from_week = serializers.IntegerField()
    to_week = serializers.IntegerField()
    username = serializers.CharField(source="group__username")

    class Meta:
        model = Schedule
        fields = ["username", "from_week", "to_week"]


class OneFieldSerializer(serializers.Serializer):
    select_field = serializers.CharField(read_only=True)
    teacher = serializers.CharField(required=False)
    subject = serializers.CharField(required=False)

    class Meta:
        model = Schedule
        fields = ["select_field", "subject", "teacher"]


class NotificationSerializer(serializers.ModelSerializer):
    data = ScheduleSerializer(many=True)
    group = serializers.CharField(max_length=255)

    class Meta:
        model = TelegramUser
        fields = ["telegram_id", "action", "data", "group"]
