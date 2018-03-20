FROM python:2.7.14-alpine3.7

RUN apk update && \
    apk add \
        g++ \
        gcc \
        libxslt-dev \
    && \
    pip install \
        lxml \
    && \
    rm -r ${HOME}/.cache/pip && \
    apk del \
        g++ \
        gcc \
        libxslt-dev \
    && \
    rm /var/cache/apk/*

