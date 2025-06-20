FROM openjdk:11

LABEL maintainer="mohana@xnatworks.io"

RUN echo "Copying files required to /usr/share" && \
    mkdir -p /usr/share


COPY ./protocolcheck /usr/share/protocolcheck


RUN echo "Setting file permissions" && \
    chmod +x /usr/share/protocolcheck/validate.sh && \
    chmod +x /usr/share/protocolcheck/validation-transform


CMD ["bash"] 
