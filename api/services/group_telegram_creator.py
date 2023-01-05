import dataclasses

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST

from users.models import GroupUserTelegram, TelegramUser


@dataclasses.dataclass
class GroupUserTelegramCreator:
    validated_data: dict

    def _get_user(self):
        return get_object_or_404(
            TelegramUser, telegram_id=self.validated_data.get("telegram_id")
        )

    def _get_obj(self, user):
        return GroupUserTelegram.objects.filter(
            user=user,
            group=self.validated_data["group"],
            token=self.validated_data["token"],
        )

    def _create(self):
        user = self._get_user()
        obj = self._get_obj(user)
        if obj:
            raise serializers.ValidationError(code=HTTP_400_BAD_REQUEST)

        instance = GroupUserTelegram(
            group=self.validated_data["group"], token=self.validated_data["token"]
        )
        instance.save()
        instance.user.add(user)
        return instance

    def execute(self):
        return self._create()
