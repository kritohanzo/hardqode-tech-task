#!/bin/sh
python manage.py migrate
python manage.py import_json -f data/users.json -a users -m User
python manage.py import_json -f data/products.json -a education -m Product
python manage.py import_json -f data/lessons.json -a education -m Lesson
python manage.py import_json -f data/lessons_products.json -a education -m LessonProduct
python manage.py import_json -f data/users_products.json -a education -m UserProduct
python manage.py collectstatic
cp -r /app/collected_static/. /backend_static/static/
gunicorn --bind 0.0.0.0:8000 backend.wsgi