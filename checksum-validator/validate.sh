#!/bin/bash

sessionId=$1
sessionLabel=$2
assignedTo=$3
scanIds=$4

scanId=${scanIds[0]}

echo "Validating $sessionLabel scans with checksums"

if [[ -z $scanId ]]; then
    cat="Missing data"
    title="No scans uploaded"
    desc="No scans uploaded for $sessionLabel"
    echo "Validation failed: no scans"
else
    cat="Wrong data"
    title="Checksum validation failed"
    desc="Checksum validation on DICOM scan $scanId failed"
    echo "Validation failed for scan $scanId"
fi

echo "Opening query..."

curl -X POST -u $XNAT_USER:$XNAT_PASS \
    --data-urlencode "status=OPEN" \
    --data-urlencode "categories=$cat" \
    --data-urlencode "title=$title" \
    --data-urlencode "description=$desc" \
    --data-urlencode "assignedto=$assignedTo" \
    "$XNAT_HOST/data/experiments/$sessionId/issues"

echo -e "\nDone"

