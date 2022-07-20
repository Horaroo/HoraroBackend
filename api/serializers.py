from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class BlockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockUser
        fields = '__all__'


class NumberWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberWeek
        fields = '__all__'
