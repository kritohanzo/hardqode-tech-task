FROM python:3.9-slim-bullseye 
WORKDIR /app
COPY requirements/requirements.project.txt .
RUN pip install -r requirements.project.txt --no-cache-dir
COPY . .
RUN chmod 700 docker_startup.sh
ENTRYPOINT ["./docker_startup.sh"] 