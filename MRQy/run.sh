#!/bin/bash

input=$1
output=$2
shift 2
scanlist=$@

cd /usr/local/bin/MRQy/src/mrqy
endpt=2
for scan in $scanlist; do
    echo "Running on scan $scan"
    python QC.py $scan /input/SCANS/$scan/DICOM
    if [[ $? -ne 0 ]]; then
        echo "MRQy failed for scan $scan" 1>&2
    else
        sed "1,$endpt d" UserInterface/Data/$scan/results.tsv >> /output/results.tsv
        if [[ $endpt == 2 ]]; then
            # only add the header once
            endpt=3
        fi
    fi
done
