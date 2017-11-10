#!/bin/bash

die(){
    echo >&2 "$@"
    exit 1
}

REF_DIR=$1
shift
FLOAT_DIR=$1
shift

REF_FILE=$(ls $REF_DIR/*.nii | head -1)
[[ -f ${REF_FILE} ]] || die "Did not find nii file in ${REF_DIR}"

FLOAT_FILE=$(ls $FLOAT_DIR/*.nii | head -1)
[[ -f ${FLOAT_FILE} ]] || die "Did not find nii file in ${FLOAT_DIR}"

echo REF_FILE=$REF_FILE
echo FLOAT_FILE=$FLOAT_FILE

echo
echo reg_aladin -ref $REF_FILE -flo $FLOAT_FILE $@
reg_aladin -ref $REF_FILE -flo $FLOAT_FILE $@ || die "Registration failed"
