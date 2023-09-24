import json

from progress.bar import PixelBar

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def add_arguments(self, parser):
        """Метод, добавляющий аргументы для команды импорта из JSON.

        Аргументы:
            -f / --file:
                Путь до файла, где хранятся данные для импорта.

            -a / --app:
                Название приложения проекта, содержащее модель для импорта.

            -m / --model:
                Название модели для импорта.
        """
        parser.add_argument("-f", "--file")
        parser.add_argument("-a", "--app")
        parser.add_argument("-m", "--model")

    def handle(self, *args, **options):
        """Метод-обработчик команды импорта."""
        app_label = options.get("app")
        model_name = options.get("model")
        model = apps.get_model(app_label=app_label, model_name=model_name)
        with open(options.get("file"), "r", encoding="utf-8") as file:
            try:
                text = json.load(file)
            except TypeError:
                try:
                    text = json.loads(file.readlines()[0])
                except TypeError:
                    raise CommandError("Получен невалидный JSON!")
            bar = PixelBar(
                f"Добавление данных в модель {model.__name__}", max=len(text)
            )
            for item in text:
                model.objects.create(**item)
                bar.next()
        bar.finish()
        self.stdout.write(self.style.SUCCESS("Добавление закончено успешно!"))
