from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "is_staff", "is_superuser"]
    list_display_links = ["id", "username"]
    search_fields = ["username", "email"]
    empty_value_display = "-"
