from enum import Enum


class UserModelConfig(Enum):
    USERNAME_MAX_LENGTH = 16
    USERNAME_VERBOSE_NAME = "Логин"
    EMAIL_MAX_LENGTH = 256
    EMAIL_VERBOSE_NAME = "Почта"
    IS_STAFF_VERBOSE_NAME = "Персонал"
    MODEL_VERBOSE_NAME = "Пользователь"
    MODEL_VERBOSE_NAME_PLURAL = "Пользователи"

class PruductModelConfig(Enum):
    NAME_MAX_LENGTH = 256
    NAME_VERBOSE_NAME = "Название"
    OWNER_VERBOSE_NAME = "Владалец"
    OWNER_RELATED_NAME = "owner_products"
    MODEL_VERBOSE_NAME = "Продукт"
    MODEL_VERBOSE_NAME_PLURAL = "Продукты"

class LessonModelConfig(Enum):
    NAME_MAX_LENGTH = 256
    NAME_VERBOSE_NAME = "Название"
    LINK_TO_VIDEO_VERBOSE_NAME = "Ссылка на видео"
    VIEWING_DURATION_VERBOSE_NAME = "Длительность просмотра"
    MODEL_VERBOSE_NAME = "Урок"
    MODEL_VERBOSE_NAME_PLURAL = "Уроки"

class UserProductModelConfig(Enum):
    USER_VERBOSE_NAME = "Пользователь"
    USER_RELATED_NAME = "user_products"
    PRODUCT_VERBOSE_NAME = "Продукт"
    PRODUCT_RELATED_NAME = "product_users"
    MODEL_VERBOSE_NAME = "Участие пользователя в продукте"
    MODEL_VERBOSE_NAME_PLURAL = "Участия пользователей в продукте"
