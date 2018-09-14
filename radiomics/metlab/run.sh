#!/bin/bash

die(){
    echo >&2 "$@"
    exit 1
}

project=$1
subject=$2
session_id=$3
session_label=$4

echo "Running metlab"
echo "metlab_wrapper.sh $XNAT_HOST $XNAT_USER $XNAT_PASS $project $subject"
metlab_wrapper.sh $XNAT_HOST $XNAT_USER $XNAT_PASS $project $subject || die "metlab_wrapper.sh failed"
echo "Done running metlab"

pushd ./*/

# Check if metlab XML file exists
metlab_xml=$(ls *.xml)
if [[ ! -e $metlab_xml ]]; then
    die "Could not find metlab XML file where I expected it."
fi

echo
echo "Creating assessor XML"
echo "create-radiomics-assessor.py $XNAT_HOST $XNAT_USER $XNAT_PASS $project $session_id $session_label $metlab_xml"
create-radiomics-assessor.py $XNAT_HOST $XNAT_USER $XNAT_PASS $project $session_id $session_label $metlab_xml || die "Failed to create metlab assessors"
echo "Done creating assessor XML"
