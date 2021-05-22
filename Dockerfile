FROM python:3.7

RUN pip install requirements.txt

COPY . /app
WORKDIR /app

CMD exec gunicorn app:app --preload -b :8080
