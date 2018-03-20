#!/bin/bash

# recon-all -i /input/$(ls /input | sort | head -1) -subjid 0000101_v00_mr -openmp 4 -all

# recon-all #SUBJECT_ID# #RECON_ALL_ARGS# -sd /output -i /input

function die() {
    echo >&2 "$@"
    date >&2
    exit 1
}


inputdir=$1
outputdir=$2
id=$3
label=$4
project=$5
scan_id=$6
shift 6
other_args="$@"


###########
# Start up
echo "Executing recon-all script"
echo "inputdir=${inputdir}"
echo "outputdir=${outputdir}"
echo "id=${id}"
echo "label=${label}"
echo "project=${project}"
echo "scan_id=${scan_id}"
echo "other_args=${other_args}"

inputfile=$(ls $inputdir | sort | head -1)
[[ $inputfile == "" ]] && die "Could not find an input file in input directory $inputdir"
echo "inputfile=${inputfile}"

###########
# Recon-all
echo
echo "Starting recon-all"
date
cmd="recon-all -i ${inputdir}/${inputfile} -sd ${outputdir} -subjid ${label} ${other_args}"
echo ${cmd}
${cmd} || die "Recon-all failed"

echo "Finished recon-all"
date

###########
# Generate assessor XML
assessor_id="${id}_freesurfer_$(date +%Y%m%d%H%M%S)"

echo
echo "Generating assessor XML"
date
cmd="stats2xml_fs5.3.pl -p ${project} -x ${session_id} -t Freesurfer -f ${assessor_id} -m ${scan_id} /output/${session_label}/stats"
echo ${cmd}
${cmd} || die "Failed to generate assessor XML"
popd
echo "Finished generating assessor XML"
date