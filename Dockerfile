FROM python:3.11

ENV PYTHONDONTEWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app_django

COPY . /app_django

RUN pip install -U pip
RUN pip install -r requirements.txt