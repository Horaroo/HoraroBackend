class BaseMixin:
    @staticmethod
    def get_menu():
        inline_buttons = {"inline_keyboard": [[], [], [], []]}
        ind = -1
        data = {
            "Быстрый старт": "quickstart",
            "Добавить токен": "add",
            "Удалить токен": "del",
            "Техническая поддержка": "help",
            "Токены": "tokens",
            "Добавить уведомление": "pin",
            "Удалить уведомление": "unpin",
        }
        for name, call_data in data.items():
            if ind == 3:
                ind = -1
            ind += 1
            inline_buttons["inline_keyboard"][ind].append(
                {"text": f"{name}", "callback_data": call_data}
            )

        return inline_buttons
