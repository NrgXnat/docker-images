FROM openjdk:8

MAINTAINER Charlie Moore <moore.c@wustl.edu>

ENV GROOVY_VERSION 2.4.7
ENV GROOVY_HOME /usr/local/groovy
ENV PATH $PATH:$GROOVY_HOME/bin

RUN wget -O groovy.zip "https://dl.bintray.com/groovy/maven/apache-groovy-binary-${GROOVY_VERSION}.zip" && \
    unzip groovy.zip && \
    rm groovy.zip && \
    mv "groovy-${GROOVY_VERSION}" $GROOVY_HOME

RUN git clone https://bitbucket.org/xnatdev/xnat_populate.git
RUN cd xnat_populate && groovy PopulateXnat.groovy -h

