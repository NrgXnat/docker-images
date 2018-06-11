# Adapted from vistalab/docker/matlab https://github.com/vistalab/docker/blob/master/matlab/runtime/2015b/Dockerfile
# Download and install Matlab Compiler Runtime v9.4 (2018a)
#
# This docker file will configure an environment into which the Matlab compiler
# runtime will be installed and in which stand-alone matlab routines (such as
# those created with Matlab's deploytool) can be executed.
#
# See http://www.mathworks.com/products/compiler/mcr/ for more info.

FROM ubuntu:bionic-20180426

# Install the MCR dependencies and some things we'll need and download the MCR
# from Mathworks -silently install it
RUN apt-get -y update && apt-get -y install \
        unzip \
        xorg \
        curl \
    && \
    mkdir \
        /mcr-install \
        /opt/mcr \
    && \
    cd /mcr-install && \
    curl --fail --silent --show-error http://ssd.mathworks.com/supportfiles/downloads/R2018a/deployment_files/R2018a/installers/glnxa64/MCR_R2018a_glnxa64_installer.zip --output MCR_R2018a_glnxa64_installer.zip && \
    unzip -q MCR_R2018a_glnxa64_installer.zip && \
    ./install -destinationFolder /opt/mcr -agreeToLicense yes -mode silent && \
    cd / && \
    rm -rf mcr-install /tmp/* && \
    apt-get remove --purge --auto-remove -y \
        unzip \
        curl \
    && \
    apt-get -y clean

# Configure environment variables for MCR
ENV LD_LIBRARY_PATH=/opt/mcr/v94/runtime/glnxa64:/opt/mcr/v94/bin/glnxa64:/opt/mcr/v94/sys/os/glnxa64:/opt/mcr/v94/extern/bin/glnxa64 XAPPLRESDIR=/opt/mcr/v94/X11/app-defaults
