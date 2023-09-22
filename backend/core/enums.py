from enum import Enum


class UserModelConfig(Enum):
    USERNAME_MAX_LENGTH = 16
    EMAIL_MAX_LENGTH = 256
    USERNAME_VERBOSE_NAME = "Логин"
    EMAIL_VERBOSE_NAME = "Почта"
    IS_STAFF_VERBOSE_NAME = "Персонал"
    MODEL_VERBOSE_NAME = "Пользователь"
    MODEL_VERBOSE_NAME_PLURAL = "Пользователи"
