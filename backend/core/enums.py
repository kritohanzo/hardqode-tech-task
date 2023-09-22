from enum import Enum


class UserEnumConfig(Enum):
    USERNAME_MAX_LENGTH = 16
    EMAIL_MAX_LENGTH = 256
    USERNAME_VERBOSE_NAME = "Логин"
    EMAIL_VERBOSE_NAME = "Почта"
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    MODEL_VERBOSE_NAME = "Пользователь"
    MODEL_VERBOSE_NAME_PLURAL = "Пользователи"