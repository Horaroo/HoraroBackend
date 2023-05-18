from rest_framework import serializers

from schedules import models
from users import models as user_models


class ScheduleSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        slug_field="username",
        queryset=user_models.CustomUser.objects.all(),
    )
    day = serializers.SlugRelatedField(
        slug_field="name", queryset=models.Day.objects.all()
    )
    week = serializers.SlugRelatedField(
        slug_field="name", queryset=models.Week.objects.all()
    )
    type_pair = serializers.SlugRelatedField(
        slug_field="name", queryset=models.Type.objects.all()
    )

    class Meta:
        model = models.Schedule
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
        model = models.Type
        fields = "__all__"


class TelegramUserSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source="token.group", read_only=True)

    class Meta:
        model = user_models.TelegramUser
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
            data["token"] = user_models.CustomUser.objects.get(
                username=data["token"]
            ).pk
            self.initial_data = data
        return super().is_valid()


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = [
            "title",
            "description",
            "picture",
            "cover",
            "is_main",
            "created_at",
        ]


class ScheduleCopySerializer(serializers.Serializer):
    source_week = serializers.IntegerField()
    target_week = serializers.IntegerField()
    source_day = serializers.CharField(default=None)
    target_day = serializers.CharField(default=None)
    source_pair = serializers.IntegerField(default=None)
    target_pair = serializers.IntegerField(default=None)

    class Meta:
        fields = [
            "source_week",
            "target_week",
            "source_day",
            "target_day",
            "source_pair",
            "target_pair",
        ]


class OneFieldSerializer(serializers.Serializer):
    select_field = serializers.CharField(read_only=True)
    teacher = serializers.CharField(required=False)
    subject = serializers.CharField(required=False)

    class Meta:
        model = models.Schedule
        fields = ["select_field", "subject", "teacher"]


class NotificationSerializer(serializers.ModelSerializer):
    data = ScheduleSerializer(many=True)
    group = serializers.CharField(max_length=255)

    class Meta:
        model = user_models.TelegramUser
        fields = ["telegram_id", "action", "data", "group"]
