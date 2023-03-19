import logging

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api import models as api_models
from bots import services

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(message)s",
    level=logging.ERROR,
)

telegram_service = services.Telegram()


class BotAPIView(GenericAPIView):
    queryset = api_models.Schedule.objects.all().select_related("group")
    schema = None

    def post(self, request, *args, **kwargs):
        data = self.request.data
        try:
            telegram_service.handle(data)
        except Exception as error:
            logging.exception("Exception occurred:", error)  # write in the 'app.log' file
            telegram_service.send_error_message(data)
        return Response("Ok", status=200)
