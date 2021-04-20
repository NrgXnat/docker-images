FROM centos:7

LABEL maintainer="mohana@radiologics.com"

RUN echo "Installing Dependencies" && \
    yum -y install bc which unzip xorg flex git bison gcc cmake gcc-c++.x86_64 make automake curl tar file xz-utils build-essential wget libstdc++-static.x86_64  zip && \
    yum install epel-release -y && \
    yum install libXtst -y && \ 
    #yum install libgl1-mesa-glx -y && \
    yum install libXt.x86_64 -y && \
    yum install libXrandr.x86_64 -y && \ 
    yum install libjpeg libjpeg-devel -y && \
    yum install jq -y

# Install dcm2niix
#RUN echo "Downloading dcm2niix..." && \
#    mkdir -p /tmp/dcm2niix && \
#    wget --progress=bar:force -O /tmp/dcm2niix.tar.gz https://github.com/rordenlab/dcm2niix/archive/v1.0.20170624.tar.gz && \
#    tar -xzvf /tmp/dcm2niix.tar.gz -C /tmp/ --strip-components 1 && \
#    cd /tmp && \
#    cmake -DUSE_OPENJPEG=ON . && \
#    mkdir -p /opt/dcm2niix && \
#    make -j$(nproc) && \
#    mv bin/ /opt/dcm2niix && \
#    cd / && \
#    rm -rf /tmp/* 

# Install FSL
RUN    echo "Downloading FSL 5.0.9..." && \
    mkdir -p /opt/fsl-5.0.9 && \
    wget --progress=bar:force -O /tmp/fsl-5.0.9-centos6_64.tar.gz https://fsl.fmrib.ox.ac.uk/fsldownloads/fsl-5.0.9-centos6_64.tar.gz && \
    tar -xzvf /tmp/fsl-5.0.9-centos6_64.tar.gz -C /opt/fsl-5.0.9 --strip-components 1 && \
    rm /tmp/fsl-5.0.9-centos6_64.tar.gz && \
    rm -R /opt/fsl-5.0.9/data/first/
# Install ImageMagick
RUN    echo "Installing ImageMagick" 	 && \
    curl -sfLO http://www.imagemagick.org/download/ImageMagick-6.9.10-12.tar.gz && \
    tar -xzf ImageMagick-6.9.10-12.tar.gz && \
    cd ImageMagick-6.9.10-12 && \
    ./configure --prefix /usr/local && \
    make install && \
    cd .. && \
    rm -rf  ImageMagick* 
# Install FaceMasking scripts
RUN   echo "Installing FaceMasking" && \
   mkdir -p /opt/maskface.12.27.2017 && \
   wget --progress=bar:force -O /tmp/MaskFace.12.27.2017.nomatlab.lin64.zip ftp://ftp.nrg.wustl.edu/pub/FaceMasking/MaskFace.12.27.2017.nomatlab.lin64.zip && \
   unzip /tmp/MaskFace.12.27.2017.nomatlab.lin64.zip -d /opt/maskface.12.27.2017 && \
   /opt/maskface.12.27.2017/lin64.nomatlab/facemaskInstaller_mcr.install -mode silent -agreeToLicense yes && \
   chmod +x /opt/maskface.12.27.2017/lin64.nomatlab/bin/cmpanalyze && \
   mkdir -p /opt/facemasking_launch_script && \
   mkdir -p /opt/dcm2nii


ADD maskface_setup.sh    /opt/facemasking_launch_script/
ADD mask-scan.sh    /opt/facemasking_launch_script/
ADD mask-session.sh    /opt/facemasking_launch_script/
ADD dcm2nii_lx.zip /tmp

# Install dcm2nii
RUN echo "Installing dcm2nii" && \
    unzip /tmp/dcm2nii_lx.zip -d /opt/dcm2nii && \
    chmod +x /opt/dcm2nii/mricron_lx/dcm2nii && \
    chmod +x /opt/facemasking_launch_script/mask*.sh && \
    yum clean all


#RUN   yum -y remove flex bison gcc make cmake automake  wget 

ENV DCMNII_HOME = "/opt/dcm2nii/mricron_lx"

ENV DEFACING_HOME="/opt/maskface.12.27.2017"

ENV FSLDIR="/opt/fsl-5.0.9"

ENV PATH="${DCMNII_HOME}/bin:${FSLDIR}/bin:${DEFACING_HOME}/lin64.nomatlab/bin:${PATH}"
ENV FSLOUTPUTTYPE="NIFTI_PAIR"

#set MCR_HOME here, e.g.
ENV MCR_HOME="/usr/local/MATLAB/MATLAB_Runtime"

#set MASKFACE_MCR_HOME here, e.g.
ENV MASKFACE_MCR_HOME="/usr/local/facemasking"

ENV MASKFACE_MATLAB_ROOT="/usr/local/MATLAB"


# Global variables used by the script.
ENV FSLDIR PATH MASKFACE_HOME MASKFACE_MCR_HOME FSLOUTPUTTYPE MASKFACE_MATLAB_ROOT
  
   
CMD ["bash"]

