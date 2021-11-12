FROM python:3.7

RUN apt-get update && apt-get install -y \
        git \
        && \ 
    pip install \
        pydicom \
        numpy \
        medpy \
        matplotlib \
        scipy \
        umap \
        pandas \
        scikit-image \
        scikit-learn \
        && \
    rm -r ${HOME}/.cache/pip

RUN cd /usr/local/bin && git clone https://github.com/ccipd/MRQy.git && \
    chmod a+x /usr/local/bin/MRQy/src/mrqy/*py

RUN apt-get remove -y \
        curl \
        mercurial \
        zip \
        && \
    apt-get autoremove -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY run.sh /usr/local/bin

WORKDIR /usr/local/bin/MRQy/src/mrqy
LABEL org.nrg.commands="[{\"name\": \"MRQy\", \"description\": \"Runs the MRIQy script\", \"version\": \"1.0\", \"schema-version\": \"1.0\", \"image\": \"radiologicskate/mrqy:1.0\", \"type\": \"docker\", \"command-line\": \"/usr/local/bin/run.sh /input /output #SCANS#\", \"override-entrypoint\": true, \"mounts\": [{\"name\": \"in\", \"writable\": false, \"path\": \"/input\"}, {\"name\": \"out\", \"writable\": true, \"path\": \"/output\"}], \"environment-variables\": {}, \"ports\": {}, \"inputs\": [{\"name\": \"SCANS\", \"description\": \"Scan ids\", \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"command-line-flag\": null, \"command-line-separator\": null, \"true-value\": null, \"false-value\": null, \"multiple-delimiter\": \"space\"}], \"outputs\": [{\"name\": \"output\", \"description\": \"Output QC files\", \"required\": true, \"mount\": \"out\", \"path\": null, \"glob\": null}], \"xnat\": [{\"name\": \"mrqy-session\", \"label\": null, \"description\": \"Run MRQy with session mounted\", \"contexts\": [\"xnat:imageSessionData\"], \"external-inputs\": [{\"name\": \"session\", \"label\": null, \"description\": \"Input session\", \"type\": \"Session\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": null, \"provides-files-for-command-mount\": \"in\", \"user-settable\": null, \"load-children\": false}], \"derived-inputs\": [{\"name\": \"scan\", \"label\": \"Scan\", \"description\": null, \"type\": \"Scan\", \"matcher\": \"('DICOM' in @.resources[*].label || 'secondary' in @.resources[*].label)\", \"default-value\": null, \"required\": false, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": \"SCANS\", \"provides-files-for-command-mount\": null, \"user-settable\": true, \"load-children\": true, \"derived-from-wrapper-input\": \"session\", \"derived-from-xnat-object-property\": \"id\", \"via-setup-command\": null, \"multiple\": true}], \"output-handlers\": [{\"name\": \"output-resource\", \"accepts-command-output\": \"output\", \"via-wrapup-command\": null, \"as-a-child-of\": \"session\", \"type\": \"Resource\", \"label\": \"MRQy\", \"format\": null}]}]}]"
