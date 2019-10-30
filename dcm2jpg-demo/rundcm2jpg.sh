#!/bin/bash
set -e

#if [[ $# -ne 2 ]]; then
#    echo "Expecting 2 arguments: $0 [input dir] [output dir]" 1>&2
#    exit 1
#fi

indir=$1
outdir=$2

conf1=$3
conf2=$4
project=$5
id=$6
label=$7
shift 7
scan_id_list=$(echo $@ | sed 's/--scan=//g')

echo "Project: ${project}"
echo "Session ID: ${id}"
echo "Session label: ${label}"
echo "Scans: ${scan_id_list}"
echo "Config settings: $conf1 and \"$conf2\""

dcmdir=$outdir/dcmInput
mkdir -p $dcmdir

echo "Locating DICOM files"
cd $indir
find . -path '*/SCANS/*/DICOM/*' -not -path '*/RESOURCES/*' -not -name '*.xml' -exec cp --parent \{\} $dcmdir/ \;
cd -

echo "Beginning dcm2jpg"
/dcm4che-5.11.1/bin/dcm2jpg $dcmdir $outdir
rm -rf $dcmdir

echo "Processing complete"
