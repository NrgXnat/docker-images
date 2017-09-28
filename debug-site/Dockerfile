FROM alpine:latest

RUN apk update && apk add \
        python \
        py-pip && \
    pip install \
        docopt \
        requests && \
    apk del py-pip && \
    rm /var/cache/apk/*

COPY create-debug-project.py /usr/local/bin/

LABEL org.nrg.commands="[{\"inputs\": [{\"name\": \"project-prefix\", \"default-value\": \"DEBUG\", \"required\": true, \"replacement-key\": \"#PROJECT_PREFIX#\", \"type\": \"string\", \"description\": \"The name of the project to create (which will be postfixed with the next available _NN for N in 0-9).\"}], \"name\": \"create-debug-project\", \"command-line\": \"create-debug-project.py \$XNAT_HOST \$XNAT_USER \$XNAT_PASS #PROJECT_PREFIX#\", \"xnat\": [{\"contexts\": [\"site\"], \"name\": \"debug-site\", \"description\": \"Run the debug-site command at the site level\"}], \"version\": \"1.0\", \"schema-version\": \"1.0\", \"type\": \"docker\", \"description\": \"Runs a script to create new debug project\"}]"
