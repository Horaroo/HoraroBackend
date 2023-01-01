from django.core import validators
from django.core.validators import EmailValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r"^[A-z]{1}[A-z\d]+$"
    message = _(
        "Введите корректный логин. Допустимые символы 'латиница' и 'цифры',"
        " логин не может начинаться с цифры."
    )
    flags = 0


@deconstructible
class UnicodeGroupValidator(validators.RegexValidator):
    regex = r"^[А-я\d]+$"
    message = _(
        "Введите корректное название группы. Допустимые символы 'кириллица' и 'цифры'."
    )
    flags = 0


email_validator = EmailValidator(message="Введите корректный email ")
