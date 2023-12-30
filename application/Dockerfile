FROM python:3.9.18-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app