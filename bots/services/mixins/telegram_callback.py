import json

import requests

from bots.services import messages
from users import models

from .common import BaseMixin


class TelegramCallbacks(BaseMixin):
    def _get_quickstart_data(self):
        return {
            "text": messages.QUICKSTART_RU,
            "buttons": [[{"text": messages.MENU_RU, "callback_data": "menu"}]],
        }

    def _get_help_data(self):
        return {
            "text": messages.HELP_RU,
            "buttons": [
                [
                    {
                        "text": "Обратная связь",
                        "url": "tg://user?id=5710085464",
                        "callback_data": "---",
                    }
                ],
                [{"text": messages.MENU_RU, "callback_data": "menu"}],
            ],
        }

    def _get_tokens_data(self):
        tokens = models.CustomUser.objects.filter(verified=True)
        inline_buttons = {
            "inline_keyboard": [
                [],  # 4 rows button
                [],
                [],
                [],
                [{"text": messages.MENU_RU, "callback_data": "menu"}],
            ]
        }

        ind = -1
        for token in tokens:
            if ind == 3:
                ind = -1
            ind += 1
            inline_buttons["inline_keyboard"][ind].append(
                {
                    "text": f"{token.username}",
                    "callback_data": f"about-token:{token.username}",
                }
            )

        return {"text": "Токены ✅", "buttons": inline_buttons["inline_keyboard"]}

    def _get_about_token_data(self, callback_data):
        token = callback_data.call_data.split(":")[1]
        token = models.CustomUser.objects.filter(username=token).first()
        is_added_token = models.TelegramUserToken.objects.filter(
            token__username=token.username,
            telegram_user__telegram_id=callback_data.user_id,
        )
        total_added = models.TelegramUserToken.objects.filter(
            token__username=token
        ).count()
        result = {
            "text": f"Информация о токене:\n{'-' * 24}\n\nТокен - {token.username}\nГруппа - {token.group}\nДобавлено - {total_added}",
            "buttons": [
                [{"text": messages.MENU_TOKENS_RU, "callback_data": "menu-tokens"}]
            ],
        }

        if is_added_token:
            button_added_or_delete = [
                {
                    "text": "Удалить токен",
                    "callback_data": f"del-token:{token.username}",
                }
            ]
        else:
            button_added_or_delete = [
                {
                    "text": "Добавить токен",
                    "callback_data": f"add-token:{token.username}",
                }
            ]

        result["buttons"].insert(0, button_added_or_delete)

        return result

    def _get_data(self, callback_data):
        return self._get_quickstart_data()

    def _send_callback(self, callback_data):
        data = self._handle_callback(callback_data)
        url = (
            "https://api.telegram.org/bot5557386036:AAG6H5f_6JE5hVLYx5MH2BZLwbZ1w2lJmRw"
        )
        r = requests.get(
            url + "/editMessageText",
            params={
                "chat_id": callback_data.user_id,
                "text": data["text"],
                "message_id": callback_data.message_id,
                "reply_markup": json.dumps({"inline_keyboard": data["buttons"]}),
            },
        )

    def _delete_token(self, callback_data):
        token = callback_data.call_data.split(":")[1]
        token = models.CustomUser.objects.filter(username=token).first()
        models.TelegramUserToken.objects.filter(
            token__username=token.username,
            telegram_user__telegram_id=callback_data.user_id,
        ).delete()

    def _add_token(self, callback_data):
        token = callback_data.call_data.split(":")[1]
        token = models.CustomUser.objects.get(username=token)
        user = models.TelegramUser.objects.get(telegram_id=callback_data.user_id)
        models.TelegramUserToken.objects.create(token=token, telegram_user=user)

    @staticmethod
    def is_callback(callback):
        try:
            _ = callback["callback_query"]["from"]["id"]
            return True
        except KeyError:
            return False

    def _handle_callback(self, callback_data):
        if callback_data.call_data == "menu":
            return {
                "text": "Панель бота",
                "buttons": self.get_menu()["inline_keyboard"],
            }
        elif callback_data.call_data == "help":
            return self._get_help_data()
        elif callback_data.call_data in ("tokens", "menu-tokens"):
            return self._get_tokens_data()
        elif callback_data.call_data == "quickstart":
            return self._get_quickstart_data()

        elif callback_data.call_data == "add":
            pass
        elif callback_data.call_data == "del":
            pass

        elif callback_data.call_data == "pin":
            pass
        elif callback_data.call_data == "unpin":
            pass

        elif callback_data.call_data.startswith("about-token:"):
            return self._get_about_token_data(callback_data)
        elif callback_data.call_data.startswith("del-token:"):
            self._delete_token(callback_data)
            return self._get_about_token_data(callback_data)
        elif callback_data.call_data.startswith("add-token:"):
            self._add_token(callback_data)
            return self._get_about_token_data(callback_data)

    def send_callback(self, callback_data):
        self._send_callback(callback_data)
