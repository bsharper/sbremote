# syntax=docker/dockerfile:1

FROM python:alpine


WORKDIR /app

COPY . .

RUN python -m venv env
ENV PATH="/env/bin:$PATH" PIP_NO_CACHE_DIR=off iSPBTV_docker=True

RUN apk add bash gcc musl-dev build-base linux-headers libffi-dev rust cargo openssl-dev git avahi && \
    pip install -r requirements.txt && \
    apk del gcc musl-dev build-base linux-headers libffi-dev rust cargo openssl-dev git

CMD ["/env/bin/python3", "-u", "app_start.py"]
