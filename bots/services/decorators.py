import json
from typing import Callable

from django.conf import settings

from .telegram_dataclasses import ResponseDecorator, ResponseTelegram


API_URL = settings.API_URL_TELEGRAM


def _get_response(data: ResponseTelegram) -> ResponseDecorator:
    """Default structure's result for message"""
    url = f"{API_URL}/{data.method}"
    result = ResponseDecorator(
        params={"chat_id": data.chat_id, "text": data.text}, url=url
    )
    if data.reply_markup is None:
        return result
    result.params.update(  # we use reply_markup for commands and callbacks
        {"reply_markup": json.dumps({"inline_keyboard": data.reply_markup})}
    )
    if data.method == "editMessageText":  # it's callback method
        result.params.update({"message_id": data.message_id})
    return result


def response_wrapper(method) -> Callable:

    def wrapper(self, *args, **kwargs) -> ResponseDecorator:
        data = method(self, *args, **kwargs)
        return _get_response(data)

    return wrapper

