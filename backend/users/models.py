from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)
from django.db import models

from core.enums import UserModelConfig
from core.validators import UsernameValidator


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UsernameValidator()

    username = models.CharField(
        verbose_name=UserModelConfig.USERNAME_VERBOSE_NAME.value,
        max_length=UserModelConfig.USERNAME_MAX_LENGTH.value,
        validators=[username_validator],
        unique=True,
    )
    email = models.EmailField(
        verbose_name=UserModelConfig.EMAIL_VERBOSE_NAME.value,
        max_length=UserModelConfig.EMAIL_MAX_LENGTH.value,
        unique=True,
    )
    is_staff = models.BooleanField(
        verbose_name=UserModelConfig.IS_STAFF_VERBOSE_NAME.value, default=False
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = UserModelConfig.MODEL_VERBOSE_NAME.value
        verbose_name_plural = UserModelConfig.MODEL_VERBOSE_NAME_PLURAL.value
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_username_email"
            )
        ]
