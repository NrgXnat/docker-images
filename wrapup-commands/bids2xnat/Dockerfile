FROM python:3.8

RUN pip install \
        docopt xnatjsession \
    && \
    rm -r ${HOME}/.cache/pip

ADD bids2xnat.py /usr/local/bin
LABEL org.nrg.commands="[{\"name\": \"bids2xnat\", \"description\": \"bids2xnat wrapup command. Transforms a BIDS formatted directory into XNAT storage with BIDS and NIFTI resources.\", \"version\": \"1.3\", \"type\": \"docker-wrapup\", \"image\": \"radiologicskate/bids2xnat-wrapup:1.3\", \"command-line\": \"bids2xnat.py /input /output\"}]"
