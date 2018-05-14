FROM centos:6.8

RUN yum -y update &&\
    yum install -y \
        zlib-devel \
        bzip2-devel \
        openssl-devel \
        xz \
        wget \
        gcc \
        zip \
        unzip \
    && \
    wget http://www.python.org/ftp/python/2.7.8/Python-2.7.8.tar.xz && \
    xz -d Python-2.7.8.tar.xz && \
    tar -xvf Python-2.7.8.tar && \
    cd Python-2.7.8 && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    cd .. && \
    rm -rf Python-2.7.8* && \
    wget --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-1.4.2.tar.gz && \
    tar -xvf setuptools-1.4.2.tar.gz && \
    cd setuptools-1.4.2 && \
    python setup.py install && \
    cd .. && \
    rm -rf setuptools-1.4.2* && \
    (curl -s https://bootstrap.pypa.io/get-pip.py | python -) && \
    pip install \
        numpy \
        matplotlib \
    && \
    wget https://fsl.fmrib.ox.ac.uk/fsldownloads/fslinstaller.py && \
    export FSLDIR=/usr/local/fsl && \
    python fslinstaller.py -d ${FSLDIR} && \
    rm fslinstaller.py && \
    echo ". ${FSLDIR}/etc/fslconf/fsl.sh" >> /root/.bash_profile && \
    mkdir /usr/local/scripts

COPY /home/shared/NRG/mmilch/lib/html2ps/bin/html2ps /usr/local/bin
COPY /usr/bin/ps2pdf /usr/local/bin
COPY /home/shared/NRG/mmilch/bin/* /usr/local/bin
COPY /home/shared/NRG/mmilch/bin/CONDR /usr/local/bin
COPY /home/shared/NRG/mmilch/script/* /usr/local/scripts

ENV FSLDIR=/usr/local/fsl PATH=/usr/local/scripts:${FSLDIR}/bin:${PATH}
