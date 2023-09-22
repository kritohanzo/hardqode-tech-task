from django.contrib import admin

from core.constants import ADMIN_EMPTY_VALUE_DISPLAY, ADMIN_SITE_HEADER
from users.models import User


admin.site.site_header = ADMIN_SITE_HEADER


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "is_staff", "is_superuser"]
    list_display_links = ["id", "username"]
    search_fields = ["username", "email"]
    empty_value_display = ADMIN_EMPTY_VALUE_DISPLAY
