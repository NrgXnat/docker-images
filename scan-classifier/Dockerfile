FROM python:3.6.5-slim-stretch

RUN apt-get update && \
    apt-get -y install unzip tk curl git

RUN pip install --upgrade pip h5py
RUN pip install glob3 joblib uuid h5py==2.8.0rc1 pillow xlutils med2image scipy==1.1.0 tensorflow==1.5.0 pandas requests pydicom

RUN git clone --branch master https://github.com/HealthplusAI/python3-gdcm.git && cd python3-gdcm && dpkg -i build_1-1_amd64.deb && apt-get install -f

RUN cp /usr/local/lib/gdcm.py /usr/local/lib/python3.6/site-packages/.
RUN cp /usr/local/lib/gdcmswig.py /usr/local/lib/python3.6/site-packages/.
RUN cp /usr/local/lib/_gdcmswig.so /usr/local/lib/python3.6/site-packages/.
RUN cp /usr/local/lib/libgdcm* /usr/local/lib/python3.6/site-packages/.
RUN ldconfig

COPY retrained_graph.pb /run/retrained_graph.pb
COPY retrained_labels.txt /run/retrained_labels.txt
COPY Classifier_wholeSession.py /run/Classifier_wholeSession.py
COPY label_probability.py /run/label_probability.py
COPY DecompressDCM.py /run/DecompressDCM.py
COPY xnatSession.py /run/xnatSession.py

LABEL org.nrg.commands="[{\"name\": \"brain-scan-type-classifier-v2\", \"description\": \"Runs brain scan type classifier on session's scans.\", \"version\": \"1.0\", \"schema-version\": \"1.0\", \"image\": \"radiologicskate/brain-scan-type-classifier:latest\", \"type\": \"docker\", \"working-directory\": \"/run\", \"command-line\": \"python Classifier_wholeSession.py /input /working #SESSION_ID# #SESSION_DIR# #SCANS#\", \"mounts\": [{\"name\": \"input\", \"writable\": false, \"path\": \"/input\"}, {\"name\": \"work\", \"writable\": true, \"path\": \"/working\"}], \"environment-variables\": {}, \"ports\": {}, \"inputs\": [{\"name\": \"SESSION_ID\", \"description\": \"Session id\", \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"command-line-flag\": null, \"command-line-separator\": null, \"true-value\": null, \"false-value\": null}, {\"name\": \"SESSION_DIR\", \"description\": \"Session directory\", \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"command-line-flag\": null, \"command-line-separator\": null, \"true-value\": null, \"false-value\": null}, {\"name\": \"SCANS\", \"description\": \"Scan ids\", \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"command-line-flag\": null, \"command-line-separator\": null, \"true-value\": null, \"false-value\": null, \"multiple-delimiter\": \"quoted-space\"}], \"xnat\": [{\"name\": \"scan-classifier\", \"label\": \"Run brain scan type classifier on a session\", \"description\": \"Run brain scan type classifier with a session mounted\", \"contexts\": [\"xnat:imageSessionData\"], \"external-inputs\": [{\"name\": \"session\", \"label\": \"Session\", \"description\": \"Input session\", \"type\": \"Session\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": null, \"provides-files-for-command-mount\": \"input\", \"via-setup-command\": null, \"user-settable\": null, \"load-children\": true}], \"derived-inputs\": [{\"name\": \"session-id\", \"label\": \"Session ID\", \"description\": null, \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": \"SESSION_ID\", \"provides-files-for-command-mount\": null, \"user-settable\": false, \"load-children\": true, \"derived-from-wrapper-input\": \"session\", \"derived-from-xnat-object-property\": \"id\", \"via-setup-command\": null, \"multiple\": false}, {\"name\": \"session-dir\", \"label\": \"Session Directory\", \"description\": null, \"type\": \"string\", \"matcher\": null, \"default-value\": null, \"required\": true, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": \"SESSION_DIR\", \"provides-files-for-command-mount\": null, \"user-settable\": false, \"load-children\": true, \"derived-from-wrapper-input\": \"session\", \"derived-from-xnat-object-property\": \"directory\", \"via-setup-command\": null, \"multiple\": false}, {\"name\": \"scan\", \"label\": \"Scan\", \"description\": null, \"type\": \"Scan\", \"matcher\": \"('DICOM' in @.resources[*].label || 'secondary' in @.resources[*].label)\", \"default-value\": null, \"required\": false, \"replacement-key\": null, \"sensitive\": null, \"provides-value-for-command-input\": \"SCANS\", \"provides-files-for-command-mount\": null, \"user-settable\": true, \"load-children\": true, \"derived-from-wrapper-input\": \"session\", \"derived-from-xnat-object-property\": \"id\", \"via-setup-command\": null, \"multiple\": true}]}]}]"
