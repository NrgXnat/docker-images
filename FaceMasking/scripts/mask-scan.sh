#!/bin/bash
set -x

USER=${1}
PASS=${2}
HOST=${3}
PROJECT=${4}
SUBJECT=${5}
SESSION=${6}
SCAN=${7}
RESOURCE=${8}
REF_SCAN=${9}
BUILD_DIR=${10}
USE_BET=${11}
INVASIVENESS=${12}
THRESHOLD=${13}
SETUP_DIR=${14}
JSESSIONID=$(curl -s -k -u $USER:$PASS $HOST/data/JSESSIONID)

scan_uri=${HOST}data/projects/$PROJECT/subjects/$SUBJECT/experiments/$SESSION/scans/$SCAN


main () {
  echo "---------------------- BEGIN defacing scan $SCAN"
  setup_build_dir
  get_dicom
  # mask_face core script
  mask_dicom
  check_output
  post_dicom_orig
  post_defaced_dicom
  post_deface_qc
  echo "---------------------- Done defacing scan $SCAN"
}

setup_build_dir () {
  # Set up build space
  zip_dir=$BUILD_DIR/zips
  input_dir=$BUILD_DIR/dicom_orig/$SCAN
  output_dir=$BUILD_DIR/dicom_deface/$SCAN
  mkdir -p $zip_dir
  mkdir -p $input_dir
  mkdir -p $output_dir
  # cd into build space since files are created in executing directory
  cd $BUILD_DIR
}

get_dicom () {
  # Get the DICOM from scan in zip archive and extract
  dicom_orig_zip=$zip_dir/${SESSION}_scan${SCAN}.zip
  # Extract without directory structure
  cp /input/SCANS/$SCAN/$RESOURCE/*  $input_dir
  # Recreate zip w/o dirs to re-upload as DICOM_ORIG
  rm $dicom_orig_zip
  zip -r -j $dicom_orig_zip $input_dir
}

mask_dicom () {
  # Either pass the ref scan or leave blank to avoid coregistraion if unnecessary
  # mask_face will assume we want to use itself for registration if not specified
  if [ "$REF_SCAN" != "none" ]; then
    reference_dir=' -r $BUILD_DIR/reference/$REF_SCAN '
  fi

  cmd="${SETUP_DIR}/maskface_setup.sh; mask_face_nomatlab $input_dir -o $output_dir $reference_dir \
    -z -b $USE_BET -e 1 -s $INVASIVENESS -t $THRESHOLD -um 0 -roi 0 -ver 0"
  eval $cmd

  # Explicity check the exit status of mask_face and try a second time if failed
  exit_val="$?"
  if [ "$exit_val" -ne "0" ]; then
    echo "ERROR -- mask_face failed!"
    echo "mask_face exited with value $exit_val"
#    echo "Retrying mask_face for scan."
#    eval $cmd
     exit 101	
  fi

#  exit_val="$?"
#  if [ "$exit_val" -ne "0" ]; then
#    echo "ERROR -- mask_face failed a second time!"
#    echo "mask_face exited with value $exit_val"
#    exit 101
#  fi
}

check_output () {
  # And also check that the output exists before moving on
  dicom_deface_zip=$output_dir/${SCAN}.zip

  if [ ! -e $dicom_deface_zip ]; then
    echo "${dicom_deface_zip} does not exist after mask_face"
    echo "Exiting ..."
    exit 102
  fi
}

post_dicom_orig () {
  # POST original non-defaced DICOM back as DICOM_ORIG unless this is a rerun
  # but skip if we are already operating on DICOM_ORIG resource

  JSESSIONID=$(refresh_jsession)

  if [ $RESOURCE = "DICOM" ]; then
    uri=$scan_uri/resources/DICOM_ORIG
    curl -f -s -k --cookie "JSESSIONID=$JSESSIONID" -X PUT $uri?format=RAW
    curl -f -s -k --cookie "JSESSIONID=$JSESSIONID" -X PUT \
      $uri/files/${SCAN}.zip?extract=true -F "${SCAN}.zip=@$dicom_orig_zip"
  fi

  exit_val="$?"
  if [ "$exit_val" -ne "0" ]; then
    echo "ERROR -- Saving DICOM as DICOM_ORIG failed!"
    echo "Curl PUT exited with value $exit_val"
    exit 103
  fi
}

post_defaced_dicom () {
  JSESSIONID=$(refresh_jsession)

  dicom_uri=$scan_uri/resources/DICOM
  # Delete DICOM resource and files
  curl -f -s -k --cookie "JSESSIONID=$JSESSIONID" -X DELETE $dicom_uri?removeFiles=true
  # Recreate the resource
  curl -f -s -k --cookie "JSESSIONID=$JSESSIONID" -X PUT $dicom_uri?format=RAW
  # PUT the defaced dicoms as DICOM resource
  curl -f -s -k --cookie "JSESSIONID=$JSESSIONID" -X POST \
    $dicom_uri/files/${SCAN}.zip?extract=true -F "${SCAN}.zip=@$dicom_deface_zip"

  if [ "$?" -ne "0" ]; then
    echo "ERROR -- Saving defaced DICOM failed!"
    exit 104
  fi
}

post_deface_qc () {
  # Collect the DEFACE_QC resource and POST them
  qc_zip=$BUILD_DIR/zips/${SCAN}_deface_qc.zip
  cd $BUILD_DIR/maskface/
  cp ${SCAN}_normfilter.png study${SCAN}_normfilter.png
  cp ${SCAN}_normfilter_surf.png study${SCAN}_normfilter_surf.png
  zip $qc_zip *${SCAN}_*.png
  zip $qc_zip ${SCAN}_*.out

  JSESSIONID=$(refresh_jsession)

  qc_uri=$scan_uri/resources/DEFACE_QC
  # Try a DELETE in case already exists, harmless if it doesn't
  curl -f -s -k --cookie "JSESSIONID=$JSESSIONID" -X DELETE $qc_uri?removeFiles=true
  # Create the resource and POST files
  curl -f -s -k --cookie "JSESSIONID=$JSESSIONID" -X PUT $qc_uri?format=PNG
  curl -f -s -k --cookie "JSESSIONID=$JSESSIONID" -X POST \
    $qc_uri/files/${SCAN}_deface_qc.zip?extract=true -F "${SCAN}_deface_qc.zip=@$qc_zip"

  if [ "$?" -ne "0" ]; then
    echo "ERROR -- Saving DEFACE_QC failed!"
    exit 105
  fi
}

refresh_jsession () {
  # Check that JSESSIONID from parent proc is still good and get new one if not
  http_code=$(curl -I -s -o /dev/null -k --cookie "JSESSIONID=$JSESSIONID" \
    -w "%{http_code}" ${HOST}data/projects)

  if [[ $http_code == "200" ]]; then
    echo $JSESSIONID
  else
    echo $(curl -s -k -u $USER:$PASS ${HOST}data/JSESSIONID)
  fi
}

main

