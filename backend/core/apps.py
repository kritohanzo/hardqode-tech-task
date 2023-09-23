from django.apps import AppConfig
from django.contrib import admin
from django.contrib.auth.apps import AuthConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        admin.site.site_header = "Администрирование HardQode"
        AuthConfig.verbose_name = "Группы"
        import core.signals
