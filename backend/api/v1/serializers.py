from rest_framework import serializers

from education.models import Lesson, Product, UserLesson
from users.models import User


class ShortLessonSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода краткой информации об уроке."""

    lesson_name = serializers.CharField(source="lesson.name", read_only=True)
    link_to_video = serializers.CharField(
        source="lesson.link_to_video", read_only=True
    )
    viewing_duration = serializers.CharField(
        source="lesson.viewing_duration", read_only=True
    )
    viewed = serializers.SerializerMethodField()
    viewing_time = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            "lesson_name",
            "link_to_video",
            "viewing_duration",
            "viewed",
            "viewing_time",
        )

    def get_viewed(self, obj):
        request = self.context.get("request")
        return UserLesson.objects.get(
            user=request.user, lesson=obj.lesson
        ).viewed

    def get_viewing_time(self, obj):
        request = self.context.get("request")
        return UserLesson.objects.get(
            user=request.user, lesson=obj.lesson
        ).viewing_time


class FullLessonSerializer(ShortLessonSerializer):
    """Сериализатор для вывода полной информации об уроке."""

    date_of_last_viewing = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            "lesson_name",
            "link_to_video",
            "viewing_duration",
            "viewed",
            "viewing_time",
            "date_of_last_viewing",
        )

    def get_date_of_last_viewing(self, obj):
        request = self.context.get("request")
        return UserLesson.objects.get(
            user=request.user, lesson=obj.lesson
        ).date_of_last_viewing


class ConcreteProductSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода конкретного продукта."""

    product_name = serializers.CharField(source="product.name", read_only=True)
    owner = serializers.CharField(
        source="product.owner.username", read_only=True
    )
    lessons = FullLessonSerializer(
        source="product.product_lessons", many=True, read_only=True
    )

    class Meta:
        model = Product
        fields = ("id", "product_name", "owner", "lessons")


class AllProductSerializer(ConcreteProductSerializer):
    """Сериализатор для вывода всех продуктов."""

    lessons = ShortLessonSerializer(
        source="product.product_lessons", many=True, read_only=True
    )


class StatProductSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода статистики продуктов."""

    product_name = serializers.CharField(source="name", read_only=True)
    owner = serializers.CharField(source="owner.username", read_only=True)
    lessons_watched_count = serializers.SerializerMethodField()
    amount_of_time_watched = serializers.SerializerMethodField()
    amount_of_students = serializers.SerializerMethodField()
    product_purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "product_name",
            "owner",
            "lessons_watched_count",
            "amount_of_time_watched",
            "amount_of_students",
            "product_purchase_percentage",
        )

    def get_lessons_watched_count(self, obj):
        product_lessons = obj.product_lessons.select_related("lesson")
        user_lessons = []
        for product_lesson in product_lessons:
            for user_lesson in product_lesson.lesson.lesson_users.all():
                user_lessons.append(user_lesson)
        lesson_watched_count = 0
        for user_lesson in user_lessons:
            if user_lesson.viewed:
                lesson_watched_count += 1
        return lesson_watched_count

    def get_amount_of_time_watched(self, obj):
        product_lessons = obj.product_lessons.select_related("lesson")
        user_lessons = [
            product_lesson.lesson.lesson_users.all()
            for product_lesson in product_lessons
        ]
        time_watched = 0
        for user_lesson in user_lessons:
            time_watched += sum(
                list(map(lambda x: x.viewing_time, user_lesson))
            )
        return time_watched

    def get_amount_of_students(self, obj):
        return obj.product_users.count()

    def get_product_purchase_percentage(self, obj):
        product_users = obj.product_users.count()
        total_users = User.objects.count()
        return f"{product_users / total_users * 100}%"
