# Dockerfile
FROM python:3.11 as builder

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN python manage.py migrate
RUN python manage.py collectstatic

CMD ["python", "manage.py", "runserver" , "0.0.0.0:8000"]
