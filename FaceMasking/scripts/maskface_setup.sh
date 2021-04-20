# Source this file to enable face masking script.
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the p
done
SCRIPTDIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"


export DEFACING_HOME=/opt/maskface.12.27.2017

#set up your dcm2nii (MRICron bin) directory here

export DCMNII_HOME=/opt/dcm2nii/mricron_lx

#set up your XNAT client tools (XNATRestClient)  path here
#set up your FSL environment here (FSLDIR)
export FSLDIR=/opt/fsl-5.0.9

export PATH=${DCMNII_HOME}:${FSLDIR}/bin:${DEFACING_HOME}/lin64.nomatlab/bin:${PATH}
export FSLOUTPUTTYPE=NIFTI_PAIR

export MCR_HOME="/usr/local/MATLAB/MATLAB_Runtime"

#set MASKFACE_MCR_HOME here, e.g.
export MASKFACE_MCR_HOME="/usr/local/facemasking"

export MASKFACE_MATLAB_ROOT="/usr/local/MATLAB"


# Global variables used by the script.
export FSLDIR PATH MASKFACE_HOME MASKFACE_MCR_HOME FSLOUTPUTTYPE MASKFACE_MATLAB_ROOT

