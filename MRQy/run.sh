#!/bin/bash

input=$1
output=$2
shift 2
scanlist=$@

cd /usr/local/bin/MRQy/src/mrqy
results=/output/results.tsv
for scan in $scanlist; do
    echo "Running on scan $scan"
    python QC.py $scan /input/SCANS/$scan/DICOM
    if [[ $? -ne 0 ]]; then
        echo "MRQy failed for scan $scan" 1>&2
    else
        scanResult=UserInterface/Data/$scan/results.tsv
        if [[ ! -e $results ]]; then
            # only add the header once
            awk -F'\t' -v OFS='\t' 'NR==3 {$2="scan"; print}' $scanResult > $results
        fi
        awk -F'\t' -v OFS='\t' -v id=$scan 'NR>3 {$2=id; print}' $scanResult >> $results
    fi
done
