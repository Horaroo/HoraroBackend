from rest_framework import serializers
import users.models
from users.models import CustomUser
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.http.response import HttpResponse
from .models import *
from djoser.conf import settings as djoser_settings


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
        name = CustomUser.objects.filter(username__iexact=username.lower())
        if bool(name):
            raise serializers.ValidationError({'username': 'Groups with this name already exist.'},
                                              code=HTTP_400_BAD_REQUEST)
        groups = CustomUser.objects.filter(group__iexact=group.lower())
        if bool(groups):
            raise serializers.ValidationError({'group': 'Groups with this name already exist.'},
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


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'group', 'email')


class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = '__all__'


class NumberWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberWeek
        fields = '__all__'
