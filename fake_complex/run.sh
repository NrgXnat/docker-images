#!/bin/bash -e

die() {
    echo "@" 2>&1
    exit 1
}

input="$1"
output="$2"
scan="$3"
project="$4"
session_id="$5"
session_label="$6"
scan_id="$7"
junk="$8"
junk="$9"

echo "Input dir: $input"
echo "Output dir: ${output}"
echo "Scan dir: ${scan}"
echo "Project: ${project}"
echo "Session ID: ${session_id}"
echo "Session label: ${session_label}"
echo "Scan ID: ${scan_id}"

echo hello > /output/output.txt

if [[ $input != ${input/scan} ]]; then
    exit
fi

echo make scan
make_scan.sh $scan $session_id $scan_id

echo fake std error 1>&2

echo Done!
