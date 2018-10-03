# Adapted from vistalab/docker/matlab https://github.com/vistalab/docker/blob/master/matlab/runtime/2015b/Dockerfile
# Download and install Matlab Compiler Runtime v9.4 (2018a)
#
# This docker file will configure an environment into which the Matlab compiler
# runtime will be installed and in which stand-alone matlab routines (such as
# those created with Matlab's deploytool) can be executed.
#
# See http://www.mathworks.com/products/compiler/mcr/ for more info.

FROM ubuntu:bionic-20180821

# Install the MCR dependencies and some things we'll need and download the MCR
# from Mathworks -silently install it
RUN apt-get -y update && apt-get -y install \
        curl \
        unzip \
        xorg \
        gcc \
        gfortran \
        openjdk-8-jdk \
    && \
    mkdir \
        /mcr-install \
        /opt/mcr \
    && \
    cd /mcr-install && \
    curl --fail --silent --show-error http://ssd.mathworks.com/supportfiles/downloads/R2018b/deployment_files/R2018b/installers/glnxa64/MCR_R2018b_glnxa64_installer.zip --output MCR_R2018b_glnxa64_installer.zip && \
    unzip -q MCR_R2018b_glnxa64_installer.zip && \
    ./install -destinationFolder /opt/mcr -agreeToLicense yes -mode silent && \
    cd / && \
    rm -rf mcr-install /tmp/* && \
    apt-get remove --purge --auto-remove -y \
        curl \
        gcc \
        gfortran \
        unzip \
    && \
    apt-get -y clean

# Configure environment variables for MCR
ENV LD_LIBRARY_PATH=/opt/mcr/v95/runtime/glnxa64:/opt/mcr/v95/bin/glnxa64:/opt/mcr/v95/sys/os/glnxa64:/opt/mcr/v95/extern/bin/glnxa64 XAPPLRESDIR=/opt/mcr/v95/X11/app-defaults
