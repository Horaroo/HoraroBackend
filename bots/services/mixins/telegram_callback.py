import json
from bots.services import messages
from .common import BaseMixin
import requests


class TelegramCallbacks(BaseMixin):

    def _get_quickstart_data(self):
        return {
            'text': messages.QUICKSTART_RU,
            'buttons':
                [
                    [{'text': messages.MENU_RU, 'callback_data': 'menu'}]
                ]
        }

    def _get_help_data(self):
        return {
            'text': messages.HELP_RU,
            'buttons':
                [
                    [{'text': 'Обратная связь', 'url': 'tg://user?id=5710085464', 'callback_data': '---'}],
                    [{'text': messages.MENU_RU, 'callback_data': 'menu'}]
                ]
        }

    def _get_data(self, callback_user):
        return self._get_quickstart_data()

    def _send_callback(self, callback_user):
        data = self._handle_callback(callback_user)
        url = "https://api.telegram.org/bot5557386036:AAG6H5f_6JE5hVLYx5MH2BZLwbZ1w2lJmRw"
        r = requests.get(url + '/editMessageText',
                         params={
                             'chat_id': callback_user.user_id,
                             'text': data['text'],
                             'message_id': callback_user.message_id,
                             'reply_markup':
                                 json.dumps({"inline_keyboard": data['buttons']}),
                         })

    @staticmethod
    def is_callback(callback):
        try:
            _ = callback["callback_query"]["from"]["id"]
            return True
        except KeyError:
            return False

    def _handle_callback(self, callback_user):
        if callback_user.call_data == 'menu':
            return {'text': 'Панель бота', 'buttons': self.get_menu()['inline_keyboard']}
        elif callback_user.call_data == 'help':
            return self._get_help_data()
        elif callback_user.call_data == 'add':
            pass
        elif callback_user.call_data == 'del':
            pass
        elif callback_user.call_data == 'token':
            pass
        elif callback_user.call_data == 'pin':
            pass
        elif callback_user.call_data == 'unpin':
            pass
        elif callback_user.call_data == 'quickstart':
            return self._get_quickstart_data()

    def send_callback(self, callback_user):
        self._send_callback(callback_user)
