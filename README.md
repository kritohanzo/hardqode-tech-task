# Тестовое задание компании HardQode / API образовательного портала

### Что было сделано?
* Написаны модели, вьюсеты и сериализаторы для пользователей, продуктов, уроков и M2M таблиц;
* Версионированное API, которое в дальнешем легко расширять;
* Команда для manage.py: import_json позволяет импортировать данные в модели из JSON файлов.
* С помощью сигналов Django добавлены автовыдача статуса 'Просмотрено' для пользователя у конкретного урока, а так же автоматическое добавление пользователей в уроки, после добавления их в продукт, аналогично с удалением;
* Подключён Swagger: документация доступна по эндпоинту '/api/v1/docs/';
* Написаны тесты для API;
* Настроен Github Workflows, при пуше в ветку 'main' запускаются тесты, проверяющие код на соответствие PEP8 и работоспособность.
* Проект разворачивается в 2-ёх контейнерах: backend, nginx;
* Удобная админка с поиском и фильтрацией по полям;

## Как запустить проект локально?

### Ручной запуск:
* Клонируйте репозиторий к себе на ПК:
```
git clone https://github.com/kritohanzo/hardqode-tech-task.git
```
* Перейдите в директорию, отвечающую за backend:
```
cd hardqode-tech-task/backend
```
* Создайте новое виртуальное окружение и работайте через него:
```
python -m venv venv
source venv/Scripts/activate (для windows)
source venv/bin/activate (для linux)
```
* Установите зависимости, необходимые для запуска backend части проекта:
```
pip install -r requirements/requirements.project.txt
```
* Выполните миграции и запустите проект:
```
python manage.py migrate
python manage.py runserver
```
* Если вам нужны тестовые данные, выполните эти 5 команд:
```
python manage.py import_json -f data/users.json -a users -m Users
python manage.py import_json -f data/products.json -a education -m Product
python manage.py import_json -f data/lessons.json -a education -m Lesson
python manage.py import_json -f data/lessons_products.json -a education -m LessonProduct
python manage.py import_json -f data/users_products.json -a education -m UserProduct
```
* Откройте браузер и зайдите на '*127.0.0.1:8000/api/v1/docs/*', у вас загрузится страница проекта.
* Для просмотра тестовых запросов, по желанию, вы можете использовать файл requests.http, который лежит в папке проекта (требует расширения REST Client для VSCode).

### Автоматический запуск (Docker):
* Клонируйте репозиторий к себе на ПК:
```
git clone https://github.com/kritohanzo/hardqode-tech-task.git
```
* Перейдите в директорию репозитория:
```
cd hardqode-tech-task
```
* Запустите docker-compose, который соберёт образы на основе Dockerfile, которые лежат в папках 'backend' и 'nginx':
```
sudo docker compose -f docker-compose.yml up
```
* Откройте браузер и зайдите на '*localhost/api/v1/docs/*', у вас загрузится страница проекта.