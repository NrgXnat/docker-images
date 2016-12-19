
FROM openjdk:8-jre

COPY bin/anonymize /opt/anon/bin/anonymize

COPY bin/uber-anonService-1.0-SNAPSHOT.jar /opt/anon/bin/uber-anonService-1.0-SNAPSHOT.jar

RUN ln -s /opt/anon/bin/anonymize /usr/local/bin/anonymize

