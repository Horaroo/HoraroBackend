from djoser.compat import get_user_email_field_name
from djoser.conf import settings as djoser_settings
from djoser.serializers import UserFunctionsMixin
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST
from services import UserCreator

from .models import CustomUser


class RegisterCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "password", "group", "email")

    def create(self, validated_data):
        return UserCreator(validated_data).execute()


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")
    id = serializers.CharField(source="user.pk")
    username = serializers.CharField(source="user")
    group = serializers.CharField(source="user.group")

    class Meta:
        model = djoser_settings.TOKEN_MODEL
        fields = ("auth_token", "id", "username", "group")


class CustomSendEmailResetSerializer(serializers.Serializer, UserFunctionsMixin):
    default_error_messages = {
        "email_not_found": djoser_settings.CONSTANTS.messages.EMAIL_NOT_FOUND
    }

    def __init__(self, *args, **kwargs):
        if kwargs.get("data") and not CustomUser.objects.filter(
            email=kwargs["data"]["email"]
        ):
            raise serializers.ValidationError(
                {"email": ["Почта не зарегистрирована."]}, code=HTTP_400_BAD_REQUEST
            )

        super().__init__(*args, **kwargs)
        self.email_field = get_user_email_field_name(CustomUser)
        self.fields[self.email_field] = serializers.EmailField()
