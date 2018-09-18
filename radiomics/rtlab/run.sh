#!/bin/bash

die(){
    echo >&2 "$@"
    exit 1
}

project=$1
subject=$2
session_id=$3
session_label=$4

echo "Running rtlab"
echo "rtlab_wrapper.sh $XNAT_HOST $XNAT_USER ***** $project $subject"
rtlab_wrapper.sh $XNAT_HOST $XNAT_USER $XNAT_PASS $project $subject || die "rtlab_wrapper.sh failed"
echo "Done running rtlab"

# Check if metlab XML file exists
metlab_xml=$(find /scratch -type f -name '*.xml')
if [[ ! -e $metlab_xml ]]; then
    die "Could not find metlab XML file anywhere inside /scratch."
fi

echo
echo "Creating assessor XML"
echo "create-radiomics-assessor.py $XNAT_HOST $XNAT_USER ***** $project $session_id $session_label $metlab_xml"
create-radiomics-assessor.py $XNAT_HOST $XNAT_USER $XNAT_PASS $project $session_id $session_label $metlab_xml || die "Failed to create radiomics assessor"
echo "Done creating assessor XML"
