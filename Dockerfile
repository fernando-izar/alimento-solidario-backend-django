FROM python:3.11

ENV PYTHONDONTEWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app_django

COPY . /app_django

RUN apt-get update && apt-get install x11-xserver-utils -y

RUN pip install -U pip
RUN pip install -r requirements.txt
# RUN xauth add $(xauth -f /app_django/.Xauthority list|tail -1)
RUN ~/usr/bin/xhost +
RUN touch ~/.Xauthority