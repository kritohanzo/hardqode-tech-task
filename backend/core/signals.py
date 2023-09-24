from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from education.models import UserLesson, UserProduct


@receiver(pre_save, sender=UserLesson)
def check_viewed(sender, instance, *args, **kwargs):
    need_time = instance.lesson.viewing_duration
    viewing_time = instance.viewing_time
    if viewing_time / need_time > 0.8:
        instance.viewed = True
        instance.save


@receiver(post_save, sender=UserProduct)
def add_to_lesson(sender, instance, *args, **kwargs):
    product_lessons = instance.product.product_lessons.all()
    user_lessons = [
        UserLesson(user=instance.user, lesson=product_lesson.lesson)
        for product_lesson in product_lessons
    ]
    UserLesson.objects.bulk_create(user_lessons)


@receiver(post_delete, sender=UserProduct)
def add_to_lesson(sender, instance, *args, **kwargs):
    product_lessons = instance.product.product_lessons.all()
    for product_lesson in product_lessons:
        user_lesson = UserLesson.objects.filter(
            user=instance.user, lesson=product_lesson.lesson
        )
        user_lesson.delete()
