FROM centos:6.9

# Install dependencies for FS
# Download FS_v5.3.0 from MGH and untar to /opt
RUN yum update -y && yum -y install \
        bc \
        libgomp.x86_64 \
        perl \
        perl-core \
        tar \
        tcsh \
        wget \
        zip \
        && \
    yum clean all
RUN wget -N -qO- ftp://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/5.3.0/freesurfer-Linux-centos6_x86_64-stable-pub-v5.3.0.tar.gz | tar -xzv -C /opt \
        --exclude='freesurfer/trctrain' \
        --exclude='freesurfer/subjects/fsaverage_sym' \
        --exclude='freesurfer/subjects/fsaverage3' \
        --exclude='freesurfer/subjects/fsaverage4' \
        --exclude='freesurfer/subjects/fsaverage5' \
        --exclude='freesurfer/subjects/fsaverage6' \
        --exclude='freesurfer/subjects/cvs_avg35' \
        --exclude='freesurfer/subjects/cvs_avg35_inMNI152' \
        --exclude='freesurfer/subjects/bert' \
        --exclude='freesurfer/subjects/V1_average' \
        --exclude='freesurfer/average/mult-comp-cor' \
        --exclude='freesurfer/lib/cuda' \
        --exclude='freesurfer/lib/qt'

# Configure license
COPY license /opt/freesurfer/.license

# Configure basic freesurfer ENV
ENV OS=Linux \
    FS_OVERRIDE=0 \
    FIX_VERTEX_AREA=  \
    SUBJECTS_DIR=/output \
    FSF_OUTPUT_FORMAT=nii.gz \
    MNI_DIR=/opt/freesurfer/mni \
    LOCAL_DIR=/opt/freesurfer/local \
    FREESURFER_HOME=/opt/freesurfer \
    FSFAST_HOME=/opt/freesurfer/fsfast \
    MINC_BIN_DIR=/opt/freesurfer/mni/bin \
    MINC_LIB_DIR=/opt/freesurfer/mni/lib \
    MNI_DATAPATH=/opt/freesurfer/mni/data \
    FMRI_ANALYSIS_DIR=/opt/freesurfer/fsfast \
    PERL5LIB=/opt/freesurfer/mni/lib/perl5/5.8.5 \
    MNI_PERL5LIB=/opt/freesurfer/mni/lib/perl5/5.8.5 \
    PATH=/opt/freesurfer/bin:/opt/freesurfer/fsfast/bin:/opt/freesurfer/tktools:/opt/freesurfer/mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Configure bashrc to source FreeSurferEnv.sh
RUN bash -c ' echo -e "source $FREESURFER_HOME/FreeSurferEnv.sh &>/dev/null" >> /root/.bashrc '
