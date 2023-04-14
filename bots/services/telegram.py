
import requests

from bots.services import mixins

from .telegram_dataclasses import (
    CallbackUser,
    CommandUser,
    MessageUser,
    ResponseDecorator,
)


class Telegram(
    mixins.TelegramMessages, mixins.TelegramCallbackSettings, mixins.TelegramCommands
):
    def send_error_message(self, data):
        pass
    def _send(self, response: ResponseDecorator):
        print(response.url)
        requests.get(response.url, response.params)

    def handle(self, data):
        if self.is_message(data):
            message = MessageUser(data).execute()
            message = self.get_message(message)
            self._send(message)
        elif self.is_callback(data):
            message = CallbackUser(data).execute()
            self.send_callback(message)
        elif self.is_command(data):
            command = CommandUser(data).execute()
            command = self.get_command(command)
            self._send(command)
