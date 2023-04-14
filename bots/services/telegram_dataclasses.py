import dataclasses
import json
from typing import Any


@dataclasses.dataclass
class MessageUser:
    message: dict | None  # During initialization dict, after call None
    text: str = None
    type_chat: str = None
    is_bot: bool = None
    user_id: int = None
    chat_id: int = None
    username: str | None = None

    def execute(self):
        message = self.message["message"]
        telegram_user = message["from"]
        self.text = message["text"]
        self.type_chat = message["chat"]["type"]
        self.is_bot = telegram_user["is_bot"]
        self.user_id = telegram_user["id"]
        self.chat_id = message["chat"]["id"]
        self.message = None
        return self


@dataclasses.dataclass
class CallbackUser:
    message: dict
    message_id = int = None
    type_chat: str = None
    is_bot: bool = None
    user_id: int = None
    chat_id: int = None
    call_data: str = None
    username: str | None = None

    def execute(self):
        callback = self.message["callback_query"]
        telegram_user = callback["from"]
        self.call_data = callback["data"]
        self.type_chat = callback["message"]["chat"]["type"]
        self.is_bot = telegram_user["is_bot"]
        self.user_id = telegram_user["id"]
        self.chat_id = callback["message"]["chat"]["id"]
        self.message_id = callback["message"]["message_id"]
        return self


@dataclasses.dataclass
class CommandUser:
    message: dict | None  # During initialization dict, after call None
    command: str = None
    type_chat: str = None
    is_bot: bool = None
    user_id: int = None
    chat_id: int = None
    username: str | None = None

    def execute(self):
        message = self.message["message"]
        telegram_user = self.message["message"]["from"]
        self.type_chat = message["chat"]["type"]
        self.command = message["text"]
        self.is_bot = telegram_user["is_bot"]
        self.user_id = telegram_user["id"]
        self.chat_id = message["chat"]["id"]
        self.message = None
        return self


@dataclasses.dataclass
class MessageWithoutButton:
    pass


@dataclasses.dataclass
class MessageWithButton:
    pass


@dataclasses.dataclass
class ButtonsWithText:
    text: str
    buttons: list[list[dict[str, str]]]


@dataclasses.dataclass
class ResponseTelegram:
    text: str = None
    method: str = None
    chat_id: str = None
    message_id: str = None
    reply_markup: list = None


@dataclasses.dataclass
class ResponseDecorator:
    url: str
    params: dict
