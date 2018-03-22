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
LABEL org.nrg.commands="[{\"inputs\": [{\"required\": true, \"name\": \"SESSION_ID\", \"description\": \"ID of a session\"}, {\"required\": true, \"name\": \"SESSION_LABEL\", \"description\": \"Label of a session\"}, {\"required\": true, \"name\": \"PROJECT\", \"description\": \"Project in which session and assessor live\"}, {\"required\": true, \"name\": \"SCANS_CSV\", \"description\": \"A comma-separated list of scan IDs on the session\"}], \"name\": \"generate-test-qc-assessor\", \"command-line\": \"generate-qc-assessor.py #SESSION_ID# #SESSION_LABEL# #PROJECT# #SCANS_CSV# /mount/out.xml\", \"outputs\": [{\"path\": \"out.xml\", \"mount\": \"mount\", \"name\": \"ASSESSOR_XML\", \"description\": \"QC assessor XML file\"}], \"version\": \"1.0\", \"schema-version\": \"1.0\", \"xnat\": [{\"output-handlers\": [{\"accepts-command-output\": \"ASSESSOR_XML\", \"type\": \"Assessor\", \"name\": \"assessor\", \"as-a-child-of\": \"session\"}, {\"accepts-command-output\": \"ASSESSOR_XML\", \"type\": \"Resource\", \"name\": \"assessor_resource\", \"as-a-child-of\": \"assessor\"}], \"derived-inputs\": [{\"provides-value-for-command-input\": \"SESSION_ID\", \"derived-from-wrapper-input\": \"session\", \"name\": \"session_id\", \"derived-from-xnat-object-property\": \"id\"}, {\"provides-value-for-command-input\": \"SESSION_LABEL\", \"derived-from-wrapper-input\": \"session\", \"name\": \"session_label\", \"derived-from-xnat-object-property\": \"label\"}, {\"provides-value-for-command-input\": \"PROJECT\", \"derived-from-wrapper-input\": \"session\", \"name\": \"project\", \"derived-from-xnat-object-property\": \"project-id\"}], \"name\": \"generate-test-qc-assessor-from-session\", \"external-inputs\": [{\"type\": \"Session\", \"name\": \"session\"}], \"description\": \"Generate a test QC assessor from a session and upload it back\"}], \"mounts\": [{\"writable\": true, \"path\": \"/mount\", \"name\": \"mount\"}], \"type\": \"docker\", \"description\": \"Generate a bogus QC assessor for testing\"}]"
