FROM python:2.7.14-alpine3.7

RUN apk update && \
    apk add \
        g++ \
        gcc \
        libxslt-dev \
    && \
    pip install \
        lxml \
        requests \
    && \
    rm -r ${HOME}/.cache/pip && \
    apk del \
        g++ \
        gcc \
    && \
    rm /var/cache/apk/*

ADD generate-qc-assessor.py /usr/local/bin/
