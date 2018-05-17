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
        ImageMagick \
        csh \
        compat-libgfortran-41 \
        util-linux \
        bc \
        perl \
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
        docopt \
        lxml \
        numpy \
        matplotlib \
        requests \
    && \
    wget https://fsl.fmrib.ox.ac.uk/fsldownloads/fslinstaller.py && \
    yum -y remove \
        gcc \
        wget \
    && \
    yum -y clean all

RUN python fslinstaller.py -d /usr/local/fsl && \
    rm -rf /usr/local/fsl/data && \
    export FSLDIR=/usr/local/fsl && \
    echo ". ${FSLDIR}/etc/fslconf/fsl.sh" >> /root/.bash_profile && \
    mkdir /usr/local/scripts

COPY dependencies/bin /usr/local/bin
COPY dependencies/scripts /usr/local/scripts
COPY dependencies/lib /usr/local/lib
COPY dependencies/nil-tools/RELEASE /usr/local/bin
COPY dependencies/nil-tools/REFDIR /usr/local/etc/nil-atlases

COPY metlab /usr/local/bin/metlab


ENV RELEASE=/usr/local/bin REFDIR=/usr/local/etc/nil-atlases FSLDIR=/usr/local/fsl METLAB_HOME=/usr/local/bin/metlab
ENV PATH=/usr/local/scripts:${METLAB_HOME}:${FSLDIR}/bin:${PATH}
