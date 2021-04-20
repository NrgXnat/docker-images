#!/bin/bash
set -x

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the p
done
SETUP_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"


PROJECT=${1}
SUBJECT=${2}
SESSION=${3}
SCANTYPES=${4}
USE_BET=${5}
INVASIVENESS=${6}
THRESHOLD=${7}


USER=$XNAT_USER
PASS=$XNAT_PASS
HOST=$XNAT_HOST

BUILD_DIR=/output
FORWARD_SLASH="/"

lengthHostStr=$((${#HOST}-1))
lastChar=`echo "${HOST:$lengthHostStr:1}"`
if [ "$lastChar" != "$FORWARD_SLASH" ]; then
  HOST="${HOST}${FORWARD_SLASH}"
fi

JSESSIONID=$(curl -s -k -u $USER:$PASS ${HOST}data/JSESSIONID)

RESOURCE=DICOM
REFSCAN=none

scan_uri="${HOST}data/archive/projects/$PROJECT/subjects/$SUBJECT/experiments/$SESSION/scans?format=json&columns=ID,type"

main () {
  mask_scan_by_type
  exit 0
}


mask_scan_by_type () {
	JSESSIONID=$(refresh_jsession)
	echo $scan_uri
	echo $SCANTYPES | sed -n 1'p' | tr ',' '\n' | while read scan; do
	    echo "Processing scan of type $scan"
  	    scan_ids=($(curl -f -s -k --cookie "JSESSIONID=$JSESSIONID" $scan_uri | jq --arg SCAN "$scan"  '. |  .ResultSet["Result"][] | select(.type==$SCAN) | .ID'))
	    #For each scan id of a given type, deface the scan
	    #If the session has no scans of the given type; bail out
	    if [[ ${scan_ids[@]} ]]; then
		    # get length of an array
		    tLen=${#scan_ids[@]}
		    # use for loop read all nameservers
		    for (( i=0; i<${tLen}; i++ ));
		    do
			scan_id=`echo ${scan_ids[$i]} | tr -d '"'`
			echo "Defacing scan $scan_id now ....."
			#Get resources for this scan. If DICOM_ORIG exists, implies its a re-run. Use DICOM_ORIG for generating defaced images
			file_uri="${HOST}data/archive/projects/$PROJECT/subjects/$SUBJECT/experiments/$SESSION/scans/$scan_id/resources?format=json"
  	    		dicom_files=($(curl -f -s -k --cookie "JSESSIONID=$JSESSIONID" $file_uri | jq --arg DICOM_ORIG_LABEL "DICOM_ORIG"  '. |  .ResultSet["Result"][] | select(.label==$DICOM_ORIG_LABEL) | .label'))
			if [[ ${dicom_files[@]} ]]; then
			   RESOURCE=DICOM_ORIG
			fi
			cmd="source $SETUP_DIR/maskface_setup.sh; $SETUP_DIR/mask-scan.sh $USER $PASS $HOST $PROJECT $SUBJECT $SESSION $scan_id $RESOURCE $REFSCAN $BUILD_DIR  $USE_BET $INVASIVENESS $THRESHOLD $SETUP_DIR"
			eval $cmd
			exit_val="$?"
			if [ "$exit_val" -ne "0" ]; then
			  echo "ERROR -- mask_face failed!"
			  echo "mask-scan exited with value $exit_val"
			  echo "Retrying mask-scan for scan $scan_id"
			  eval $cmd
			fi
			exit_val="$?"
			if [ "$exit_val" -ne "0" ]; then
			  echo "ERROR -- mask-scan failed a second time!"
			  echo "mask-scan exited with value $exit_val"
			  exit 101
			fi
		    done
	    fi	    
	done
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
