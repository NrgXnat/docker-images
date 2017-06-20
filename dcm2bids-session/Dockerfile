FROM python:2.7
MAINTAINER John Flavin <jflavin@wustl.edu>

RUN apt-get update && apt-get install -y \
        curl \
        mercurial \
        pigz \
        zip \
        && \
    pip install \
        dicom \
        nipype \
        requests \
        && \
    rm -r ${HOME}/.cache/pip && \
    curl -L http://github.com/rordenlab/dcm2niix/releases/download/v1.0.20170609/dcm2niix_9-Jun-2017_lnx.zip  > dcm2niix_9-Jun-2017_lnx.zip && \
    unzip dcm2niix_9-Jun-2017_lnx.zip && \
    mv dcm2niix /usr/local/bin && \
    chmod a+x /usr/local/bin/dcm2niix && \
    rm dcm* && \
    mkdir /src && cd /src && \
    hg clone https://bitbucket.org/nrg_customizations/nrg_pipeline_dicomtobids && \
    cp nrg_pipeline_dicomtobids/scripts/catalog/DicomToBIDS/scripts/dcm2bids_wholeSession.py . && \
    cp nrg_pipeline_dicomtobids/resources/catalog/DicomToBIDS/resources/bidsmap.json . && \
    rm -r nrg_pipeline_dicomtobids && \
    apt-get remove -y \
        curl \
        mercurial \
        zip \
        && \
    apt-get autoremove -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /src

LABEL org.nrg.commands="[{\"name\": \"dcm2bids-session\", \"description\": \"Runs dcm2niix on a session's scans, and uploads the nifti and bids json\", \"version\": \"1.0\", \"schema-version\": \"1.0\", \"type\": \"docker\", \"command-line\": \"python dcm2bids_wholeSession.py #SESSION_ID# #OVERWRITE# --host \$XNAT_HOST --user \$XNAT_USER --pass \$XNAT_PASS --upload-by-ref False --dicomdir /dicom --niftidir /nifti\", \"workdir\": \"/src\", \"mounts\": [{\"name\": \"nifti\", \"writable\": \"true\", \"path\": \"/nifti\"}], \"inputs\": [{\"name\": \"session_id\", \"description\": \"XNAT ID of the session\", \"type\": \"string\", \"required\": true, \"replacement-key\": \"#SESSION_ID#\", \"command-line-flag\": \"--session\"}, {\"name\": \"overwrite\", \"description\": \"Overwrite any existing NIFTI and BIDS scan resources?\", \"type\": \"string\", \"required\": false, \"default-value\": false, \"replacement-key\": \"#OVERWRITE#\", \"true-value\": \"True\", \"false-value\": \"False\", \"command-line-flag\": \"--overwrite\"}], \"outputs\": [], \"xnat\": [{\"name\": \"dcm2bids-session-session\", \"description\": \"Run dcm2niix-session on a Session\", \"contexts\": [\"xnat:imageSessionData\"], \"external-inputs\": [{\"name\": \"session\", \"description\": \"Input session\", \"type\": \"Session\", \"required\": true}], \"derived-inputs\": [{\"name\": \"session-id\", \"description\": \"The session's id\", \"type\": \"string\", \"derived-from-xnat-input\": \"session\", \"derived-from-xnat-object-property\": \"id\", \"provides-value-for-command-input\": \"session_id\"}], \"output-handlers\": []}]}]"
