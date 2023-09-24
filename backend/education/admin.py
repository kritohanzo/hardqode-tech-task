from django import forms
from django.contrib import admin

from education.models import (
    Lesson,
    LessonProduct,
    Product,
    UserLesson,
    UserProduct,
)


class UserLessonForm(forms.ModelForm):
    class Meta:
        model = UserLesson
        fields = "__all__"

    def clean_viewing_time(self):
        # do something that validates your data
        viewing_time = self.cleaned_data["viewing_time"]
        need_time = self.cleaned_data["lesson"].viewing_duration
        if viewing_time > need_time:
            raise forms.ValidationError(
                "Время просмотра пользователем "
                "не может быть больше длины видео"
            )
        return viewing_time


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "owner"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]
    empty_value_display = "-"


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "link_to_video", "viewing_duration"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]
    empty_value_display = "-"


@admin.register(LessonProduct)
class LessonProductAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "lesson"]
    list_display_links = ["id", "product", "lesson"]
    search_fields = ["product", "lesson"]
    empty_value_display = "-"


@admin.register(UserProduct)
class UserProductAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product"]
    list_display_links = ["id", "user", "product"]
    search_fields = ["user", "product"]
    empty_value_display = "-"


@admin.register(UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    form = UserLessonForm
    list_display = [
        "id",
        "user",
        "lesson",
        "viewing_time",
        "viewed",
        "date_of_last_viewing",
    ]
    list_display_links = ["id", "user", "lesson"]
    search_fields = ["user", "lesson"]
    empty_value_display = "-"
