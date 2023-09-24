from enum import Enum


class UserModelConfig(Enum):
    """Конфигурация модели пользователя."""

    USERNAME_MAX_LENGTH = 16
    USERNAME_VERBOSE_NAME = "Логин"
    EMAIL_MAX_LENGTH = 256
    EMAIL_VERBOSE_NAME = "Почта"
    IS_STAFF_VERBOSE_NAME = "Персонал"
    MODEL_VERBOSE_NAME = "Пользователь"
    MODEL_VERBOSE_NAME_PLURAL = "Пользователи"


class PruductModelConfig(Enum):
    """Конфигурация модели продукта."""

    NAME_MAX_LENGTH = 256
    NAME_VERBOSE_NAME = "Название"
    OWNER_VERBOSE_NAME = "Владалец"
    OWNER_RELATED_NAME = "owner_products"
    MODEL_VERBOSE_NAME = "Продукт"
    MODEL_VERBOSE_NAME_PLURAL = "Продукты"


class LessonModelConfig(Enum):
    """Конфигурация модели урока."""

    NAME_MAX_LENGTH = 256
    NAME_VERBOSE_NAME = "Название"
    LINK_TO_VIDEO_VERBOSE_NAME = "Ссылка на видео"
    VIEWING_DURATION_VERBOSE_NAME = "Длительность просмотра"
    MODEL_VERBOSE_NAME = "Урок"
    MODEL_VERBOSE_NAME_PLURAL = "Уроки"


class LessonProductModelConfig(Enum):
    """Конфигурация модели урока-продукта."""

    PRODUCT_VERBOSE_NAME = "Продукт"
    PRODUCT_RELATED_NAME = "product_lessons"
    LESSON_VERBOSE_NAME = "Урок"
    LESSON_RELATED_NAME = "lesson_products"
    MODEL_VERBOSE_NAME = "Наличие урока в продукте"
    MODEL_VERBOSE_NAME_PLURAL = "Наличия уроков в продукте"


class UserProductModelConfig(Enum):
    """Конфигурация модели пользователя-продукта."""

    USER_VERBOSE_NAME = "Пользователь"
    USER_RELATED_NAME = "user_products"
    PRODUCT_VERBOSE_NAME = "Продукт"
    PRODUCT_RELATED_NAME = "product_users"
    MODEL_VERBOSE_NAME = "Участие пользователя в продукте"
    MODEL_VERBOSE_NAME_PLURAL = "Участия пользователей в продуктах"


class UserLessonModelConfig(Enum):
    """Конфигурация модели пользователя-урока."""

    USER_VERBOSE_NAME = "Пользователь"
    USER_RELATED_NAME = "user_lessons"
    LESSON_VERBOSE_NAME = "Урок"
    LESSON_RELATED_NAME = "lesson_users"
    VIEWING_TIME_VERBOSE_NAME = "Время просмотра"
    VIEWED_VERBOSE_NAME = "Просмотрено"
    DATE_OF_LAST_VIEWING_VERBOSE_NAME = "Дата последнего просмотра"
    MODEL_VERBOSE_NAME = "Участие пользователя в уроке"
    MODEL_VERBOSE_NAME_PLURAL = "Участия пользователей в уроках"
