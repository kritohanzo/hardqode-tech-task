from django.db import models

from core.enums import (
    LessonModelConfig,
    LessonProductModelConfig,
    PruductModelConfig,
    UserLessonModelConfig,
    UserProductModelConfig,
)
from users.models import User


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
        null=True,
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


class LessonProduct(models.Model):
    product = models.ForeignKey(
        to=Product,
        verbose_name=LessonProductModelConfig.PRODUCT_VERBOSE_NAME.value,
        related_name=LessonProductModelConfig.PRODUCT_RELATED_NAME.value,
        on_delete=models.CASCADE,
    )
    lesson = models.ForeignKey(
        to=Lesson,
        verbose_name=LessonProductModelConfig.LESSON_VERBOSE_NAME.value,
        related_name=LessonProductModelConfig.LESSON_RELATED_NAME.value,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = LessonProductModelConfig.MODEL_VERBOSE_NAME.value
        verbose_name_plural = (
            LessonProductModelConfig.MODEL_VERBOSE_NAME_PLURAL.value
        )

    def __str__(self):
        return f"{self.lesson} - урок продукта {self.product}"


class UserProduct(models.Model):
    user = models.ForeignKey(
        to=User,
        verbose_name=UserProductModelConfig.USER_VERBOSE_NAME.value,
        related_name=UserProductModelConfig.USER_RELATED_NAME.value,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        to=Product,
        verbose_name=UserProductModelConfig.PRODUCT_VERBOSE_NAME.value,
        related_name=UserProductModelConfig.PRODUCT_RELATED_NAME.value,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = UserProductModelConfig.MODEL_VERBOSE_NAME.value
        verbose_name_plural = (
            UserProductModelConfig.MODEL_VERBOSE_NAME_PLURAL.value
        )

    def __str__(self):
        return f"{self.user} - участник продукта {self.product}"


class UserLesson(models.Model):
    user = models.ForeignKey(
        to=User,
        verbose_name=UserLessonModelConfig.USER_VERBOSE_NAME.value,
        related_name=UserLessonModelConfig.USER_RELATED_NAME.value,
        on_delete=models.CASCADE,
    )
    lesson = models.ForeignKey(
        to=Lesson,
        verbose_name=UserLessonModelConfig.LESSON_VERBOSE_NAME.value,
        related_name=UserLessonModelConfig.LESSON_RELATED_NAME.value,
        on_delete=models.CASCADE,
    )
    viewing_time = models.PositiveIntegerField(
        verbose_name=UserLessonModelConfig.VIEWING_TIME_VERBOSE_NAME.value,
        default=0,
    )
    viewed = models.BooleanField(
        verbose_name=UserLessonModelConfig.VIEWED_VERBOSE_NAME.value,
        default=False,
    )
    date_of_last_viewing = models.DateField(
        verbose_name=(
            UserLessonModelConfig.DATE_OF_LAST_VIEWING_VERBOSE_NAME.value
        ),
        auto_now=True,
    )

    class Meta:
        verbose_name = UserLessonModelConfig.MODEL_VERBOSE_NAME.value
        verbose_name_plural = (
            UserLessonModelConfig.MODEL_VERBOSE_NAME_PLURAL.value
        )

    def __str__(self):
        return f"{self.user} - участник урока {self.lesson}"
