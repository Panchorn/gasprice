FROM python:3.7

RUN pip install requirements.txt

COPY . /app
WORKDIR /app

ENV PORT 8080
CMD exec gunicorn app:app --preload --bind :$PORT
