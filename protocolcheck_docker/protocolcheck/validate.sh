#!/bin/bash
set -x

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the p
done
tool_home="$( cd -P "$( dirname "$SOURCE" )" && pwd )"


#Expected variables from environment

#buildir=/Users/TEST/build
#XNAT_HOST=http://localhost:8080
#XNAT_USER=admin
#XNAT_PASS=admin

#Expected variables from command line

## xnat_project
## sessionLabel
## session
## subjectlabel
## session_type
## catalog_content
## rulefile
## notify - expected 1 or 2
## projectSpecificSiteImportFileExists - expected 0 or 1
## xnatserver

xnat_project=${1}
sessionLabel=${2}
session=${3}
subjectlabel=${4}
session_type=${5}
catalog_content=${6}
rulefile=${7}
notify=${8}
projectSpecificSiteImportsFileExists=${9}
xnatserver=${10}


tool_home=/usr/share/protocolcheck

xslfile=$tool_home/svrl/nrg_iso_svrl_for_xslt2.xsl
site_import_xslfile=$tool_home/site_imports.xsl
datatype=$(echo "$session_type" | tr ":" "_")
collection="validation_"$datatype
workdir=${buildir}/$sessionLabel
validationfolder=${workdir}/VALIDATION
experimentfile=${validationfolder}/${sessionLabel}".xml"
rulexslfile=${validationfolder}/${sessionLabel}"_rule.xsl"
reportfile=${validationfolder}/${sessionLabel}"_report.xml"
emailreportfile=${validationfolder}/${sessionLabel}"_email.txt"
validationfile=${validationfolder}/${sessionLabel}"_validation.xml"
now=$(date +'%Y%m%d_%H%M%S')
validation_id=${sessionLabel}"_PC_"${now}
validationxslfile=${tool_home}/create_validate.xsl
emailxslfile=${tool_home}/create_text_attachment.xsl


## GET JSESSION

j_session=$(curl -u $XNAT_USER:$XNAT_PASS -X POST ${XNAT_HOST}/data/JSESSION)


main() {
  validate
  exit 0
}

validate () {


##Step 0 - Prepare Rule Folder

mkdir -p $validationfolder

##Step 0a - Get Experiment XML from XNAT

$(curl --cookie "JSESSIONID=$j_session" -o ${experimentfile} -X GET "${XNAT_HOST}/data/experiments/${session}?format=xml") 

##Step 0b - Get Rule File

$(curl --cookie "JSESSIONID=${j_session}" -o ${validationfolder}/${rulefile} -X GET "${XNAT_HOST}/REST/projects/${xnat_project}/resources/${collection}/files/${rulefile}") 

##Step 1a - Get default site_import xsl file

cp ${site_import_xslfile} ${validationfolder}/site_imports.xsl

##Step 1b - Get Project specific site import file
if [[ "$projectSpecificSiteImportsFileExists" == "1" ]]; then
$(curl --cookie "JSESSIONID=${j_session}" -o ${validation_folder}/site_imports.xsl -X GET "${XNAT_HOST}/data/archive/projects/${xnat_project}/resources/${collection}/files/site_imports.xsl") 
fi

## Step 1 - Generate the Intermediate XSL file which would check the rules

${tool_home}/validation-transform -o $rulexslfile ${validationfolder}/$rulefile $xslfile

## Step 2 - Generate report file by applying rule file to Experiment XML
${tool_home}/validation-transform -o $reportfile $experimentfile $rulexslfile experimentfilename=${experimentfile} xnat_user=$XNAT_USER xnat_host=$XNAT_HOST xnat_password=$XNAT_PASS xnat_jsession=${j_session}

## Step 3 - Generate validation xml file
${tool_home}/validation-transform -o $validationfile $reportfile $validationxslfile reportfilename=$reportfile rulefilename=$rulefile rulexslfilename=$rulexslfile xslfilename=$xslfile experimentfilename=$experimentfile xnat_user=$XNAT_USER xnat_host=$XNAT_HOST xnat_password=$XNAT_PASS xnat_jsession=$j_session validationfilename=$validationfile validationxslfilename=$validationxslfile  uri_content=$catalog_content validation_id=$validation_id

## Step 3a - Generate Email report file
${tool_home}/validation-transform -o $emailreportfile $reportfile $emailxslfile xnatserver=$xnatserver 


j_session=$(refresh_jsession)


## Step 4 - Upload the validation document

$(curl -s --cookie "JSESSIONID=${j_session}" -X PUT "${XNAT_HOST}/data/archive/projects/${xnat_project}/subjects/${subjectlabel}/experiments/$session/assessors/$validation_id?inbody=true&event_reason=Standard%20Processing&event_type=PROCESS&event_action=Create%20assessor" --data-binary "@$validationfile")

## Step 4a - Create out catalog
##$(curl -s --cookie "JSESSIONID=${j_session}" -X PUT "$XNAT_HOST/data/archive/projects/$xnat_project/subjects/$subjectlabel/experiments/$session/assessors/$validation_id/out/resources/VALIDATION?event_reason=Standard%20Processing&event_type=PROCESS&event_action=Create%20resource")

## Step 4b - Upload rule file

$(curl -s --cookie "JSESSIONID=${j_session}" -X PUT "$XNAT_HOST/data/archive/projects/$xnat_project/subjects/$subjectlabel/experiments/$session/assessors/$validation_id/out/resources/VALIDATION/files/$rulefile?content=RULEFILE&inbody=true&event_reason=Standard%20Processing&event_type=PROCESS&event_action=Create%20resource" --data-binary "@${validationfolder}/${rulefile}") 

## Step 4c - Upload the report file used

$(curl -s --cookie "JSESSIONID=${j_session}" -X PUT "$XNAT_HOST/data/archive/projects/$xnat_project/subjects/$subjectlabel/experiments/$session/assessors/$validation_id/out/resources/VALIDATION/files/${sessionLabel}_report.xml?content=REPORTFILE&req_format=TEXT&inbody=true&event_reason=Standard%20Processing&event_type=PROCESS&event_actioCreate%20resource" --data-binary "@$reportfile")

## Step 4d - Upload the log file

#$(curl -s --cookie "JSESSIONID=${j_session}" -X PUT "$XNAT_HOST/data/archive/projects/$xnat_project/subjects/$subjectlabel/expeirments/$session/assessors/$validation_id/out/resources/VALIDATION/files/${sessionLabel}_validation.log?content=LOGFILE&req_format=TEXT&inbody=true&event_reason=Standard%20Processing&event_type=PROCESS&event_action=Create%20resource" --data-binary "@$vliadtion_logfile")

## Step 4e - Upload the err file

#$(curl -s --cookie "JSESSION=${j_session}" -X PUT "$XNAT_HOST/data/archive/projects/$xnat_project/subjects/$subjectalabel/experiments/$session/assessors/$validation_id/out/resources/VALIDATION/files/${sessionLabel}_validation.err?content=ERRFILE&req_format=TEXT&inbody=true&event_reason=Standard%20Processing&event_type=PROCESS&event_action=Create%20resource" --data-binary "@$validation_errorfile") 

}

refresh_jsession () {
  # Check that JSESSIONID from parent proc is still good and get new one if not
  http_code=$(curl -I -s -o /dev/null -k --cookie "JSESSIONID=$j_session" \
    -w "%{http_code}" "${XNAT_HOST}/data/projects")

  if [[ $http_code == "200" ]]; then
    echo $j_session
  else
    echo $(curl -s -k -u $XNAT_USER:$XNAT_PASS ${XNAT_HOST}/data/JSESSIONID)
  fi
}



main


