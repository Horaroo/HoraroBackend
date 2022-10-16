from rest_framework import serializers
from .models import *
from djoser.conf import settings as djoser_settings
from django.db.models import Q
from rest_framework.status import HTTP_400_BAD_REQUEST
from djoser.serializers import UserFunctionsMixin
from djoser.compat import get_user_email_field_name
from users.models import TelegramUser, GroupUserTelegram
from django.shortcuts import get_object_or_404


class RegisterCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "password",
            "group",
            "email"
        )

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        group = validated_data["group"]
        email = validated_data["email"]
        groups = CustomUser.objects.filter(group=group)
        if bool(groups):
            raise serializers.ValidationError({'group': ['Группа с таким именем уже зарегистрирована.']},
                                              code=HTTP_400_BAD_REQUEST)

        user = CustomUser(username=username, email=email, group=group)
        user.set_password(password)
        user.save()
        return user


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")
    id = serializers.CharField(source="user.pk")
    username = serializers.CharField(source="user")
    group = serializers.CharField(source="user.group")

    class Meta:
        model = djoser_settings.TOKEN_MODEL
        fields = ("auth_token", "id", "username", 'group')


class CustomSendEmailResetSerializer(serializers.Serializer, UserFunctionsMixin):
    default_error_messages = {
        "email_not_found": djoser_settings.CONSTANTS.messages.EMAIL_NOT_FOUND
    }

    def __init__(self, *args, **kwargs):
        if kwargs.get('data') and not CustomUser.objects.filter(email=kwargs['data']['email']):
            raise serializers.ValidationError({'email': ['Почта не зарегистрирована.']},
                                              code=HTTP_400_BAD_REQUEST)

        super().__init__(*args, **kwargs)
        self.email_field = get_user_email_field_name(CustomUser)
        self.fields[self.email_field] = serializers.EmailField()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'group', 'email')


class NumberWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberWeek
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('number_pair',
                  'subject',
                  'teacher',
                  'audience',
                  'week',
                  'group',
                  'type_pair',
                  'day')

    def create(self, validated_data):
        group = validated_data['group']
        number = validated_data['number_pair']
        week = validated_data['week']
        day = validated_data['day']
        obj = Schedule.objects.filter(Q(number_pair=number) & Q(week=week) & Q(group=group) & Q(day=day))
        if bool(obj):
            instance = obj.first()
            instance.subject = validated_data.get('subject', instance.subject)
            instance.teacher = validated_data.get('teacher', instance.subject)
            instance.audience = validated_data.get('audience', instance.audience)
            instance.type_pair = validated_data.get('type_pair', instance.type_pair)
            instance.save()
            return instance
        else:
            return Schedule.objects.create(**validated_data)


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class TelegramUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TelegramUser
        fields = [
            'telegram_id',
            'username',
            'is_moder',
            'token',
            'action',
            'notification_time'
        ]

    def is_valid(self, raise_exception=False):
        data = self.initial_data.dict()
        if data.get('token'):
            data['token'] = CustomUser.objects.get(username=data['token']).pk
            self.initial_data = data
        return super().is_valid()


class GroupUserTelegramSerializer(serializers.ModelSerializer):
    telegram_id = serializers.CharField(write_only=True)

    class Meta:
        model = GroupUserTelegram
        fields = ['group', 'telegram_id', 'token']

    def create(self, validated_data):
        user = get_object_or_404(TelegramUser, telegram_id=validated_data.get('telegram_id'))
        obj = GroupUserTelegram.objects.filter(user=user, group=validated_data['group'], token=validated_data['token'])
        if obj:
            raise serializers.ValidationError(code=HTTP_400_BAD_REQUEST)
        instance = GroupUserTelegram(group=validated_data['group'], token=validated_data['token'])
        instance.save()
        instance.user.add(user)
        return instance


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'picture', 'cover', 'is_main', 'created_at']


class ScheduleCopySerializer(serializers.ModelSerializer):
    from_week = serializers.IntegerField()
    to_week = serializers.IntegerField()
    username = serializers.CharField(source='group__username')

    class Meta:
        model = Schedule
        fields = ['username', 'from_week', 'to_week']


class OneFieldSerializer(serializers.Serializer):
    select_field = serializers.CharField(read_only=True)
    teacher = serializers.CharField(required=False)
    subject = serializers.CharField(required=False)

    class Meta:
        model = Schedule
        fields = [
            'select_field',
            'subject',
            'teacher'
        ]


class NotificationSerializer(serializers.ModelSerializer):
    data = ScheduleSerializer(many=True)
    group = serializers.CharField(max_length=255)

    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'action', 'data', 'group']
