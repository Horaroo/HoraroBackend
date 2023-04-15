
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
        requests.get(response.url, response.params)

    def handle(self, data):
        response = None
        if self.is_message(data):
            message = MessageUser(data).execute()
            response = self.get_message(message)
        elif self.is_callback(data):
            message = CallbackUser(data).execute()
            response = self.get_callback(message)
        elif self.is_command(data):
            command = CommandUser(data).execute()
            response = self.get_command(command)
        if response:
            self._send(response)
