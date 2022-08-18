from rest_framework import serializers
from users.models import CustomUser, Group
from .models import *
from djoser.conf import settings as djoser_settings
from django.db.models import Q


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
        group = int(validated_data["group"])
        email = validated_data["email"]
        name = CustomUser.objects.filter(username__iexact=username.lower())
        # if bool(name):
        #     raise serializers.ValidationError({'username': 'Groups with this name already exist.'},
        #                                       code=HTTP_400_BAD_REQUEST)
        # groups = CustomUser.objects.filter(group__iexact=group.lower())
        # if bool(groups):
        #     raise serializers.ValidationError({'group': 'Имя с'},
        #                                       code=HTTP_400_BAD_REQUEST)
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
