from .common import BaseMixin


class TelegramCommands(BaseMixin):
    @staticmethod
    def is_command(message):
        try:
            _ = message["message"]["entities"][0]["type"] == "bot_command"
            return True
        except KeyError:
            return False

    def get_commands(self, command_user):
        return self.get_menu()
