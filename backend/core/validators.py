from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^[a-z0-9_]+\Z"
    message = (
        "Имя пользователя должно состоять только из строчных "
        "английских букв, цифр или знака подчёркивания!"
    )
    flags = 0
