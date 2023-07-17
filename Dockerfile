# syntax=docker/dockerfile:1

FROM python:alpine

VOLUME /data
WORKDIR /app

COPY . .

RUN apk add bash && \
    apk del gcc musl-dev build-base linux-headers libffi-dev rust cargo openssl-dev git

ENTRYPOINT ["python", "-u", "app_start.py"]
