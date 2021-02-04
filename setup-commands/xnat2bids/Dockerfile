FROM python:3.8

RUN pip install \
        docopt pathlib xnatbidsfns \
    && \
    rm -r ${HOME}/.cache/pip

ADD dummy_dataset_description.json /root/dataset_description.json
ADD xnat2bids.py /usr/local/bin
LABEL org.nrg.commands="[{\"name\": \"xnat2bids\", \"description\": \"xnat2bids setup command. Transforms an XNAT session with BIDS and NIFTI resources into BIDS format.\", \"version\": \"1.4\", \"type\": \"docker-setup\", \"image\": \"radiologicskate/xnat2bids-setup:1.4\", \"command-line\": \"xnat2bids.py /input /output\"}]"
