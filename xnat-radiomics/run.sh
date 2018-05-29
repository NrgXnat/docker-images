#!/bin/bash

die(){
    echo >&2 "$@"
    exit 1
}

project=$1
subject=$2
session_id=$3
session_label=$4

metlab_wrapper.sh $XNAT_HOST $XNAT_USER $XNAT_PASS $project $subject || die "metlab_wrapper.sh failed"

pushd ./*/

# Check if metlab XML file exists
metlab_xml=$(ls *.xml)
if [[ ! -e $metlab_xml ]]; then
    die "Could not find metlab XML file where I expected it."
fi

create-radiomics-assessor.py $XNAT_HOST $XNAT_USER $XNAT_PASS $project $session_id $session_label $metlab_xml || die "Failed to create metlab assessors"

