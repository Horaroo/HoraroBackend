import json

from django.conf import settings

from .telegram_dataclasses import ResponseDecorator, ResponseTelegram


class ResponseWrapper:
    API_URL = settings.API_URL_TELEGRAM

    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs) -> ResponseDecorator:
        data = self._func(*args, **kwargs)
        return self._get_response(data)

    def _get_response(self, data: ResponseTelegram) -> ResponseDecorator:
        """Default structure's result for message"""
        url = f"{self.API_URL}/{data.method}"
        result = ResponseDecorator(
            params={"chat_id": data.chat_id, "text": data.text}, url=url
        )
        result.params.update(  # we use reply_markup for commands and callbacks
            {"reply_markup": json.dumps({"inline_keyboard": data.reply_markup})}
        )
        if data.method == "editMessageText":  # it's callback method
            result.params.update({"message_id": data.message_id})
        return result
