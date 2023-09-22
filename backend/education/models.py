from django.db import models
from users.models import User
from core.enums import (
    PruductModelConfig,
    LessonModelConfig,
    UserProductModelConfig,
)


class Product(models.Model):
    name = models.CharField(
        verbose_name=PruductModelConfig.NAME_VERBOSE_NAME.value,
        max_length=PruductModelConfig.NAME_MAX_LENGTH.value,
    )
    owner = models.ForeignKey(
        to=User,
        verbose_name=PruductModelConfig.OWNER_VERBOSE_NAME.value,
        related_name=PruductModelConfig.OWNER_RELATED_NAME.value,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = PruductModelConfig.MODEL_VERBOSE_NAME.value
        verbose_name_plural = (
            PruductModelConfig.MODEL_VERBOSE_NAME_PLURAL.value
        )

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(
        verbose_name=LessonModelConfig.NAME_VERBOSE_NAME.value,
        max_length=LessonModelConfig.NAME_MAX_LENGTH.value,
    )
    link_to_video = models.URLField(
        verbose_name=LessonModelConfig.LINK_TO_VIDEO_VERBOSE_NAME.value
    )
    viewing_duration = models.PositiveIntegerField(
        verbose_name=LessonModelConfig.VIEWING_DURATION_VERBOSE_NAME.value
    )

    class Meta:
        verbose_name = LessonModelConfig.MODEL_VERBOSE_NAME.value
        verbose_name_plural = LessonModelConfig.MODEL_VERBOSE_NAME_PLURAL.value

    def __str__(self):
        return self.name


class ProductLesson(models.Model):
    ...


class UserProduct(models.Model):
    user = models.ForeignKey(
        to=User,
        verbose_name=UserProductModelConfig.USER_VERBOSE_NAME.value,
        related_name=UserProductModelConfig.USER_RELATED_NAME.value,
    )
    product = models.ForeignKey(
        to=Product,
        verbose_name=UserProductModelConfig.PRODUCT_VERBOSE_NAME.value,
        related_name=UserProductModelConfig.PRODUCT_RELATED_NAME.value,
    )

    class Meta:
        verbose_name = UserProductModelConfig.MODEL_VERBOSE_NAME.value
        verbose_name_plural = (
            UserProductModelConfig.MODEL_VERBOSE_NAME_PLURAL.value
        )

    def __str__(self):
        return f"{self.user} - участник продукта {self.product}"