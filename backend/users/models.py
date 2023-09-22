from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from core.enums import UserEnumConfig


class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name=UserEnumConfig.USERNAME_VERBOSE_NAME.value, max_length=UserEnumConfig.USERNAME_MAX_LENGTH.value, unique=True
    )
    email = models.EmailField(
        verbose_name=UserEnumConfig.EMAIL_VERBOSE_NAME.value, max_length=UserEnumConfig.EMAIL_MAX_LENGTH.value, unique=True
    )

    EMAIL_FIELD = UserEnumConfig.EMAIL_FIELD.value
    USERNAME_FIELD = UserEnumConfig.USERNAME_FIELD.value
    REQUIRED_FIELDS = UserEnumConfig.REQUIRED_FIELDS.value

    class Meta:
        verbose_name = UserEnumConfig.MODEL_VERBOSE_NAME.value
        verbose_name_plural = UserEnumConfig.MODEL_VERBOSE_NAME_PLURAL.value
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique appversion"
            )
        ]