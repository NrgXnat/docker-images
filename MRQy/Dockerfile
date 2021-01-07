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
    chmod a+x /usr/local/bin/MRQy/*py

RUN apt-get remove -y \
        curl \
        mercurial \
        zip \
        && \
    apt-get autoremove -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /usr/local/bin/MRQy
LABEL org.nrg.commands="[{\"name\": \"MRQy\", \"description\": \"Runs the MRIQy script\", \"version\": \"1.0\", \"schema-version\": \"1.0\", \"image\": \"radiologicskate/mrqy:1.0\", \"type\": \"docker\", \"command-line\": \"python QC.py /output /input\", \"override-entrypoint\": true, \"mounts\": [{\"name\": \"in\", \"writable\": false, \"path\": \"/input\"}, {\"name\": \"out\", \"writable\": true, \"path\": \"/output\"}], \"environment-variables\": {}, \"ports\": {}, \"inputs\": [], \"outputs\": [{\"name\": \"output\", \"description\": \"Output QC files\", \"required\": true, \"mount\": \"out\", \"path\": null, \"glob\": null}], \"xnat\": [{\"name\": \"mrqy-session\", \"label\": null, \"description\": \"Run MRQy with session mounted\", \"contexts\": [\"xnat:imageSessionData\"], \"external-inputs\": [{\"name\": \"session\", \"label\": null, \"description\": \"Input session\", \"type\": \"Session\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": null, \"provides-files-for-command-mount\": \"in\", \"user-settable\": null, \"load-children\": false}], \"derived-inputs\": [], \"output-handlers\": [{\"name\": \"output-resource\", \"accepts-command-output\": \"output\", \"via-wrapup-command\": null, \"as-a-child-of\": \"session\", \"type\": \"Resource\", \"label\": \"MRQy\", \"format\": null}]}, {\"name\": \"mrqy-project\", \"label\": null, \"description\": \"Run MRQy with project mounted\", \"contexts\": [\"xnat:projectData\"], \"external-inputs\": [{\"name\": \"project\", \"label\": null, \"description\": \"Input project\", \"type\": \"Project\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": null, \"provides-files-for-command-mount\": \"in\", \"user-settable\": null, \"load-children\": false}], \"derived-inputs\": [], \"output-handlers\": [{\"name\": \"output-resource\", \"accepts-command-output\": \"output\", \"via-wrapup-command\": null, \"as-a-child-of\": \"project\", \"type\": \"Resource\", \"label\": \"MRQy\", \"format\": null}]}]}]"
