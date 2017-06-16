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
    groovy -Dgroovy.grape.report.downloads=true PopulateXnat.groovy -h

LABEL org.nrg.commands="[{\"name\": \"simple_populate\", \"version\": \"1.1\", \"working-directory\": \"/xnat_populate\", \"type\": \"docker\", \"command-line\": \"groovy PopulateXnat.groovy -u \$XNAT_USER -p \$XNAT_PASS --url \$XNAT_HOST -d #project_list#\", \"inputs\": [{\"name\": \"project_list\", \"type\": \"string\"}], \"xnat\": [{\"name\": \"empty_wrapper\"}]}, \
    {\"name\": \"populate_with_site_config\", \"version\": \"1.1\", \"working-directory\": \"/xnat_populate\", \"type\": \"docker\", \"command-line\": \"groovy PopulateXnat.groovy -u \$XNAT_USER -p \$XNAT_PASS --url \$XNAT_HOST -d #project_list# -g #config_file#\", \"inputs\": [{\"name\": \"project_list\", \"type\": \"string\"}, {\"name\": \"config_file\", \"type\": \"string\"}], \"xnat\": [{\"name\": \"empty_wrapper\"}]}]"
