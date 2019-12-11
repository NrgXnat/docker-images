FROM python:2.7.14-alpine3.6

RUN pip install \
        docopt \
    && \
    rm -r ${HOME}/.cache/pip

ADD xnat2bids.py /usr/local/bin
LABEL org.nrg.commands="[{\"name\": \"xnat2bids\", \"description\": \"xnat2bids setup command. Transforms an XNAT session with BIDS and NIFTI resources into BIDS format.\", \"version\": \"1.2\", \"type\": \"docker-setup\", \"image\": \"radiologicskate/xnat2bids-setup:1.2\", \"command-line\": \"xnat2bids.py /input /output\"}]"
