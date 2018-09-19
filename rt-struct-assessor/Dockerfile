FROM python:3.7.0-alpine3.7

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

LABEL org.nrg.commands="[{\"inputs\": [{\"required\": true, \"type\": \"string\", \"name\": \"SUBJ_ID\", \"description\": \"Subject ID\"}, {\"required\": true, \"type\": \"string\", \"name\": \"SESS_ID\", \"description\": \"Session ID\"}, {\"required\": true, \"type\": \"string\", \"name\": \"SESS_LABEL\", \"description\": \"Session Label\"}, {\"required\": true, \"type\": \"string\", \"name\": \"PROJ\", \"description\": \"Project\"}, {\"required\": true, \"type\": \"string\", \"name\": \"RT_FILE_NAME\", \"description\": \"Name of DICOM RT-STRUCT file\"}, {\"required\": false, \"name\": \"DELAY\", \"default-value\": \"0\", \"description\": \"Delay finishing execution to give snapshot generation time to finish. (This is a hack.)\"}], \"name\": \"make-rt-struct-assessor\", \"command-line\": \"make-rt-struct-assessor.py #SUBJ_ID# #SESS_ID# #SESS_LABEL# #PROJ# /input/#RT_FILE_NAME# /output/assessor.xml #DELAY#\", \"outputs\": [{\"path\": \"assessor.xml\", \"mount\": \"out\", \"required\": true, \"name\": \"xml\", \"description\": \"The assessor XML\"}, {\"path\": \"#RT_FILE_NAME#\", \"mount\": \"in\", \"required\": true, \"name\": \"dicom-rt\", \"description\": \"The DICOM RT-STRUCT file\"}], \"version\": \"1.2\", \"schema-version\": \"1.0\", \"xnat\": [{\"derived-inputs\": [{\"load-children\": false, \"derived-from-wrapper-input\": \"scan\", \"type\": \"Session\", \"name\": \"session\", \"required\": true}, {\"provides-value-for-command-input\": \"SESS_ID\", \"derived-from-wrapper-input\": \"session\", \"type\": \"string\", \"name\": \"session-id\", \"derived-from-xnat-object-property\": \"id\"}, {\"provides-value-for-command-input\": \"SESS_LABEL\", \"derived-from-wrapper-input\": \"session\", \"type\": \"string\", \"name\": \"session-label\", \"derived-from-xnat-object-property\": \"label\"}, {\"provides-value-for-command-input\": \"SUBJ_ID\", \"derived-from-wrapper-input\": \"session\", \"type\": \"string\", \"name\": \"subject-id\", \"derived-from-xnat-object-property\": \"subject-id\"}, {\"provides-value-for-command-input\": \"PROJ\", \"derived-from-wrapper-input\": \"session\", \"type\": \"string\", \"name\": \"project\", \"derived-from-xnat-object-property\": \"project-id\"}, {\"matcher\": \"@.label == 'DICOM' || @.label == 'secondary'\", \"derived-from-wrapper-input\": \"scan\", \"type\": \"Resource\", \"name\": \"scan-dicom\", \"provides-files-for-command-mount\": \"in\"}, {\"derived-from-wrapper-input\": \"scan-dicom\", \"type\": \"File\", \"name\": \"scan-dicom-rt-struct-file\"}, {\"provides-value-for-command-input\": \"RT_FILE_NAME\", \"derived-from-wrapper-input\": \"scan-dicom-rt-struct-file\", \"type\": \"string\", \"name\": \"scan-dicom-rt-struct-file-name\", \"derived-from-xnat-object-property\": \"name\"}], \"contexts\": [\"xnat:imageScanData\"], \"description\": \"Run the make-rt-struct-assess container from a scan\", \"output-handlers\": [{\"accepts-command-output\": \"xml\", \"type\": \"Assessor\", \"name\": \"assessor\", \"as-a-child-of\": \"session\"}, {\"accepts-command-output\": \"dicom-rt\", \"type\": \"Resource\", \"name\": \"assessor-resource\", \"as-a-child-of\": \"assessor\", \"label\": \"RTSTRUCT\"}], \"external-inputs\": [{\"matcher\": \"\", \"required\": true, \"type\": \"Scan\", \"name\": \"scan\", \"description\": \"RT-STRUCT scan\"}], \"name\": \"make-rt-struct-assessor-from-rt-struct-scan\"}], \"mounts\": [{\"writable\": \"true\", \"path\": \"/output\", \"name\": \"out\"}, {\"writable\": \"false\", \"path\": \"/input\", \"name\": \"in\"}], \"type\": \"docker\", \"description\": \"Create an RoiCollection assessor from a DICOM RT-STRUCT scan\"}]"
