#!/bin/bash
set -e

if [[ $# -ne 2 ]]; then
    echo "Expecting 2 arguments: $0 [input dir] [output dir]" 1>&2
    exit 1
fi

indir=$1
outdir=$2

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
