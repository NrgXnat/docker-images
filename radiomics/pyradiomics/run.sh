#!/bin/bash -e

die() {
    echo "@" 2>&1
    exit 1
}

scan="$1"
shift
mask="$1"
shift
output="$1"
shift
project="$1"
shift
session_id="$1"
shift
session_label="$1"
shift
scan_id="$1"
shift
mask_file_uri="$1"

echo "Scan file: ${scan}"
echo "Mask file: ${mask}"
echo "Output dir: ${output}"
echo "Project: ${project}"
echo "Session ID: ${session_id}"
echo "Session label: ${session_label}"
echo "Scan ID: ${scan_id}"
echo "Mask File URI: ${mask_file_uri}"

if [[ $mask = *" "* ]]
then
	echo "Mask name: \"${mask}\" may not contain spaces."
	echo "Halting execution."
	exit 1
fi
 

# # Begin constructing CSV batch file
# batch_file="/tmp/batch.csv"
# echo "Image,Mask,Label" > ${batch_file}


# mask_file_name=$(basename $mask)
# echo "Mask file name: $mask_file_name"
#
# echo "Running find-mask-value ${mask}"
# mask_label_value=$(find-mask-value ${mask})
# echo "Mask label value: $mask_label_value"

# echo "${scan},${mask},${mask_label_value}" >> ${batch_file}

echo
echo "Running pyradiomics"
echo "pyradiomics ${scan} ${mask} --param /usr/src/pyradiomics/examples/exampleSettings/exampleMR_3mm.yaml --verbosity 5 --out ${output}/pyradiomics.csv --format-path basename --format csv"
pyradiomics ${scan} ${mask} --param /usr/src/pyradiomics/examples/exampleSettings/exampleMR_3mm.yaml --verbosity 5 --out ${output}/pyradiomics.csv --format-path basename --format csv || die "pyradiomics failed"

echo

echo "Generating assessor"
echo "generate-pyradiomics-xml-from-csv $XNAT_HOST $project $session_id $session_label $scan_id $mask_file_uri ${output}/pyradiomics.csv ${output}/pyradiomics.xml"
generate-pyradiomics-xml-from-csv $XNAT_HOST $project $session_id $session_label $scan_id $mask_file_uri ${output}/pyradiomics.csv ${output}/pyradiomics.xml || die "failed to generate assessor"

echo
echo "All done"
