from rest_framework import serializers
from users.models import CustomUser, Group
from .models import *
from djoser.conf import settings as djoser_settings
from django.db.models import Q
from rest_framework.status import HTTP_400_BAD_REQUEST
from djoser.serializers import UserFunctionsMixin
from djoser.compat import get_user_email_field_name


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


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


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
