FROM python:3.6.5-alpine3.7

RUN apk add --update \
        g++ \
        gcc \
        libxslt-dev \
    && \
    pip install \
        docopt \
        lxml \
        pydicom \
    && \
    apk del --purge \
        gcc \
        g++ \
    && \
    rm -r /var/cache/apk/* && \
    rm -r ${HOME}/.cache/pip

COPY make-rt-struct-assessor.py /usr/local/bin
