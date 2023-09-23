from django.db.models.signals import pre_save
from django.dispatch import receiver

from education.models import UserLesson


@receiver(pre_save, sender=UserLesson)
def check_viewed(sender, instance, *args, **kwargs):
    need_time = instance.lesson.viewing_duration
    viewing_time = instance.viewing_time
    if viewing_time / need_time > 0.8:
        instance.viewed = True
        instance.save
