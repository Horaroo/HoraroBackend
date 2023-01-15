
class TelegramMessages:

    @staticmethod
    def is_message(message):
        try:
            _ = message["message"]["from"]["id"]
            return not str(message["message"]["text"]).startswith('/')
        except KeyError:
            return False

    def send_message(self, message_user):
        pass

