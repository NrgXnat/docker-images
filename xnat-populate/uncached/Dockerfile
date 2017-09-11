FROM openjdk:8

MAINTAINER Charlie Moore <moore.c@wustl.edu>

ENV GROOVY_VERSION=2.4.7 \
    GROOVY_HOME=/usr/local/groovy
ENV PATH=$PATH:$GROOVY_HOME/bin

RUN wget -O groovy.zip "https://dl.bintray.com/groovy/maven/apache-groovy-binary-${GROOVY_VERSION}.zip" && \
    unzip groovy.zip && \
    rm groovy.zip && \
    mv "groovy-${GROOVY_VERSION}" $GROOVY_HOME

RUN git clone --progress --verbose http://bitbucket.org/xnatdev/xnat_populate.git && \
    cd xnat_populate && \
    git checkout tags/4.1.3 && \
    groovy -Dgroovy.grape.report.downloads=true PopulateXnat.groovy -h

LABEL org.nrg.commands="[{\"name\": \"xnat_populate\", \"version\": \"2.0\", \"working-directory\": \"/xnat_populate\", \"type\": \"docker\", \"command-line\": \"groovy PopulateXnat.groovy -u \$XNAT_USER -p \$XNAT_PASS --url \$XNAT_HOST #project_list# #config# #delay#\", \"inputs\": [{\"name\": \"project_list\", \"description\": \"A comma-separated list of known projects to populate this XNAT with (or the name of one of the standard text files containing a list of projects).\", \"command-line-flag\": \"-d\", \"type\": \"string\", \"required\": true}, {\"name\": \"config\", \"description\": \"The filename for one of the standard provided configuration YAML files.\", \"command-line-flag\": \"-g\", \"type\": \"string\"}, {\"name\": \"delay\", \"description\": \"Delay in milliseconds to wait after each session upload.\", \"command-line-flag\": \"-w\", \"type\": \"number\"}], \"xnat\": [{\"name\": \"xnat_populate\"}]}]"
