#!/bin/bash
#
#~ND~FORMAT~MARKDOWN~
#~ND~START~
#
# ## COPYRIGHT NOTICE
#
# Copyright (C) 2015 Anticevic Lab, Yale University
# Copyright (C) 2015 MBLAB, University of Ljubljana
#
# ## AUTHORS(s)
#
# * Alan Anticevic, Department of Psychiatry, Yale University
#
# ## PRODUCT
#
#  MNAPAcceptanceTest.sh
#
# ## LICENSE
#
# * The MNAPAcceptanceTest.sh = the "Software"
# * This Software conforms to the license outlined in the MNAP Suite:
# * https://bitbucket.org/hidradev/mnaptools/src/master/LICENSE.md
#
# ## TODO
#
#
# ## DESCRIPTION 
#   
# This script, MNAPAcceptanceTest.sh, implements MNAP acceptance testing per pipeline unit.
# 
# ## PREREQUISITE INSTALLED SOFTWARE
#
# * curl
#
# ## PREREQUISITE ENVIRONMENT VARIABLES
#
# See output of usage function: e.g. $./MNAPAcceptanceTest.sh --help
#
# ## PREREQUISITE PRIOR PROCESSING
# 
# * The necessary input files are data stored in the following format
# * These data are stored in: "$SubjectsFolder/$CASE/
#
#~ND~END~

# ------------------------------------------------------------------------------
# -- General help usage function
# ------------------------------------------------------------------------------

SupportedAcceptanceTestSteps="hcp1 hcp2 hcp3 hcp4 hcp5 BOLDImages"

usage() {
    echo ""
    echo "-- DESCRIPTION:"
    echo ""
    echo "This function implements MNAP acceptance testing per pipeline unit."
    echo ""
    echo ""
    echo "-- REQUIRED PARMETERS:"
    echo ""
    echo "-- Local system variables if using MNAP hierarchy:"
    echo ""
    echo ""
    echo "   --acceptancetest=<request_acceptance_test>    Specify if you wish to run a final acceptance test after each unit of processing."
    echo "                                                      Supported: ${SupportedAcceptanceTestSteps}"
    echo ""
    echo "   --studyfolder=<path_to_mnap_study>            Path to study data folder"
    echo "   --subjectsfolder=<folder_with_subjects_data>  Path to study data folder where the subjects folders reside"
    echo "   --subjects=<list_of_cases>                    List of subjects to run that are study-specific and correspond to XNAT database subject IDs"
    echo "   --sessionlabels=<imaging_session_labels>      Label for session within project. Note: may be general across multiple subjects (e.g. rest) or for longitudinal runs."
    echo "   --runtype=<local_or_xnat_check>               Default is [], which executes a local file system run, but requires --studyfolder to set"
    echo ""
    echo ""
    echo "-- XNAT PARAMETERS:"
    echo ""
    echo "   Note: To invoke this function you need a credential file in your home folder or provide one " 
    echo "         using --xnatcredentials parameter or --xnatuser and --xnatpass parameters: " 
    echo ""
    echo "    --xnatcredentialfile=<xnat_credential_file_name> Specify XNAT credential file name."
    echo "                                                     Default: ${HOME}/.xnat    "
    echo "                                                     This file stores the username and password for the XNAT site"
    echo "                                                     Permissions of this file need to be set to 400"
    echo "                                                     If this file does not exist the script will prompt you to generate one using default name"
    echo "                                                     If user provided a file name but it is not found, this name will be used to generate new credentials"
    echo "                                                     User needs to provide this specific credential file for next run, as script by default expects ${HOME}/.xnat"
    echo "" 
    echo "    --xnatprojectid=<name_of_xnat_project_id>        Specify the XNAT site project id. This is the Project ID in XNAT and not the Project Title."
    echo "                                                        This project should be created on the XNAT Site prior to upload."
    echo "                                                        If it is not found on the XNAT Site or not provided then the data will land into the prearchive and be left unassigned to a project."
    echo "                                                        Please check upon completion and specify assignment manually."
    echo "    --xnathost=<XNAT_site_URL>                       Specify the XNAT site hostname URL to push data to."
    echo ""
    echo "    --xnatuser=<xnat_host_user_name>                 Specify XNAT username required if credential file is not found"
    echo "    --xnatpass=<xnat_host_user_pass>                 Specify XNAT password required if credential file is not found"
    echo "    --bidsformat=<specify_bids_input>                Specify if XNAT data is in BIDS format (yes/no). Default is [no]"
    echo "                                                        If --bidsformat='yes' then the subject naming follows <SubjectLabel_SessionLabel> convention"
    echo ""
    echo "    --xnatsubjectid=<xnat_subject_id>                ID for subject across the entire XNAT database. * Required or --xnatsubjectlabels needs to be set."
    echo "    --xnatsubjectlabels=<xnat_subject_label>         Label for subject within a project for the XNAT database. Default assumes it matches --subjects."
    echo "                                                     If your XNAT database subject label is distinct from your local server subject id then please supply this flag."
    echo "                                                     Use if your XNAT database has a different set of subject ids."
    echo "    --xnatsessionlabels=<xnat_session_labels>        Label for session within XNAT project. Note: may be general across multiple subjects (e.g. rest). * Required."
    echo "    --xnataccsessionid=<xnat_accesession_id>         ID for subject-specific session within the XNAT project. * Derived from XNAT but can be set manually."
    echo ""
    echo "    --resetcredentials=<reset_credentials_for_xnat_site_>  Specify <yes> if you wish to reset your XNAT site user and password. Default is [no]"
    echo ""
    echo "    --xnatgetqc=<download_qc_images_locally>               Specify if you wish to download QC PNG images and/or scene files for a given acceptance unit where QC is available. Default is [no]"
    echo "                                                           Options: "
    echo "                                                                     --xnatgetqc='image'   --> download only the image files "
    echo "                                                                     --xnatgetqc='scene'   --> download only the scene files" 
    echo "                                                                     --xnatgetqc='all'     --> download both png images and scene files"
    echo ""
    echo "    --xnatarchivecommit=<commit_acceptance_test_to_xnat>   Specify if you wish to commit the results of acceptance testing back to the XNAT archive. Default is [no]"
    echo "                                                           Options: "
    echo "                                                                     --xnatarchivecommit='session' --> commit to subject session only "
    echo "                                                                     --xnatarchivecommit='project' --> commit group results to project only" 
    echo "                                                                     --xnatarchivecommit='all'     --> commit both subject and group results"
    echo ""
    echo ""
    echo "-- BOLD PROCESSING ACCEPTANCE TEST PARAMETERS:"
    echo ""
    echo "--bolddata=<bold_run_numbers>                                    Specify BOLD data numbers separated by comma or pipe. E.g. --bolddata='1,2,3,4,5' "
    echo "                                                                   This flag is interchangeable with --bolds or --boldruns to allow more redundancy in specification"
    echo "                                                                   Note: If unspecified empty the QC script will by default look into /<path_to_study_subjects_folder>/<subject_id>/subject_hcp.txt and identify all BOLDs to process"
    echo ""    
    echo "--boldimages=<bold_run_numbers>                                  Specify a list of required BOLD images separated by comma or pipe. Where the number of the bold image would be, indicate by '{N}', e.g:"
    echo "                                                                   --boldimages='bold{N}_Atlas.dtseries.nii|seed_bold{N}_Atlas_g7_hpss_res-VWMWB_lpss_LR-Thal.dtseriesnii' "
    echo "                                                                   When running the test, '{N}' will be replaced by the bold numbers given in --bolddata "
    echo ""
    echo "-- Example:"
    echo ""
    echo "MNAPAcceptanceTest.sh --studyfolder='<absolute_path_to_study_folder>' \ "
    echo "--subjects='<subject_IDs_on_local_server>' \ "
    echo "--xnatprojectid='<name_of_xnat_project_id>' \ "
    echo "--xnathost='<XNAT_site_URL>' "
    echo ""
}

# ------------------------------------------------------------------------------
# -- Check for help
# ------------------------------------------------------------------------------

if [[ $1 == "" ]] || [[ $1 == "--help" ]] || [[ $1 == "-help" ]] || [[ $1 == "--usage" ]] || [[ $1 == "-usage" ]] || [[ $1 == "help" ]] || [[ $1 == "usage" ]]; then
    usage
fi

# ------------------------------------------------------------------------------
# -- Setup color outputs
# ------------------------------------------------------------------------------

reho() {
    echo "\033[31m $1 \033[0m"
}

geho() {
    echo "\033[32m $1 \033[0m"
}

ceho() {
    echo "\033[36m $1 \033[0m"
}

# ------------------------------------------------------------------------------
# -- Parse and check all arguments
# ------------------------------------------------------------------------------

# -- Set general options functions
opts_GetOpt() {
sopt="$1"
shift 1
for fn in "$@" ; do
    if [ `echo ${fn} | grep -- "^${sopt}=" | wc -w` -gt 0 ]; then
        echo "${fn}" | sed "s/^${sopt}=//"
        return 0
    fi
done
}

opts_CheckForHelpRequest() {
for fn in "$@" ; do
    if [ "$fn" = "--help" ]; then
        return 0
    fi
done
}

if [ $(opts_CheckForHelpRequest $@) ]; then
    showVersion
    show_usage
    exit 0
fi

# -- Initialize global output variables
unset CASES
unset StudyFolder
unset SubjectsFolder
unset SESSION_LABELS
unset BOLDS # --bolddata
unset BOLDRUNS # --bolddata
unset BOLDDATA # --bolddata
unset BOLDImages # --boldimages

unset XNAT_HOST_NAME
unset XNAT_USER_NAME
unset XNAT_PASSWORD
unset XNAT_PROJECT_ID

unset XNAT_ACCSESSION_ID
unset XNAT_SUBJECT_ID
unset XNAT_SUBJECT_LABEL
unset XNAT_SUBJECT_LABELS
unset XNAT_SESSION_LABELS
unset XNAT_CREDENTIALS
unset XNAT_CREDENTIAL_FILE
unset XNATgetQC
unset XNATArchiveCommit
unset XNATResetCredentials

unset AcceptanceTestSteps
unset BIDSFormat
unset RUN_TYPE



# -- Parse general arguments
StudyFolder=`opts_GetOpt "--studyfolder" $@`
CASES=`opts_GetOpt "--subjects" "$@" | sed 's/,/ /g;s/|/ /g'`; CASES=`echo "$CASES" | sed 's/,/ /g;s/|/ /g'`
SESSION_LABELS=`opts_GetOpt "--sessionlabel" "$@" | sed 's/,/ /g;s/|/ /g'`; SESSION_LABELS=`echo "$SESSION_LABELS" | sed 's/,/ /g;s/|/ /g'`
if [[ -z ${SESSION_LABELS} ]]; then
SESSION_LABELS=`opts_GetOpt "--sessionlabels" "$@" | sed 's/,/ /g;s/|/ /g'`; SESSION_LABELS=`echo "$SESSION_LABELS" | sed 's/,/ /g;s/|/ /g'`
fi
RUN_TYPE=`opts_GetOpt "--runtype" $@`
AcceptanceTestSteps=`opts_GetOpt "--acceptancetests" "$@" | sed 's/,/ /g;s/|/ /g'`; AcceptanceTestSteps=`echo "$AcceptanceTestSteps" | sed 's/,/ /g;s/|/ /g'`
if [[ -z ${AcceptanceTestSteps} ]]; then
AcceptanceTestSteps=`opts_GetOpt "--acceptancetest" "$@" | sed 's/,/ /g;s/|/ /g'`; AcceptanceTestSteps=`echo "$AcceptanceTestSteps" | sed 's/,/ /g;s/|/ /g'`
fi

# -- Parse BOLD arguments
BOLDS=`opts_GetOpt "--bolds" "$@" | sed 's/,/ /g;s/|/ /g'`; BOLDS=`echo "${BOLDS}" | sed 's/,/ /g;s/|/ /g'`
if [ -z "${BOLDS}" ]; then
    BOLDS=`opts_GetOpt "--boldruns" "$@" | sed 's/,/ /g;s/|/ /g'`; BOLDS=`echo "${BOLDS}" | sed 's/,/ /g;s/|/ /g'`
fi
if [ -z "${BOLDS}" ]; then
    BOLDS=`opts_GetOpt "--bolddata" "$@" | sed 's/,/ /g;s/|/ /g'`; BOLDS=`echo "${BOLDS}" | sed 's/,/ /g;s/|/ /g'`
fi
BOLDRUNS="${BOLDS}"
BOLDDATA="${BOLDS}"
BOLDSuffix=`opts_GetOpt "--boldsuffix" $@`
BOLDPrefix=`opts_GetOpt "--boldprefix" $@`
BOLDImages=`opts_GetOpt "--boldimages" "$@" | sed 's/,/ /g;s/|/ /g'`; BOLDImages=`echo "${BOLDImages}" | sed 's/,/ /g;s/|/ /g'`

# -- If data is in BIDS format on XNAT
BIDSFormat=`opts_GetOpt "--bidsformat" $@`

# -- Start of parsing XNAT arguments
#
#     INFO ON XNAT VARIABLE MAPPING FROM MNAP --> JSON --> XML specification
#
# project               --xnatprojectid        #  --> mapping in MNAP: XNAT_PROJECT_ID     --> mapping in JSON spec: #XNAT_PROJECT#   --> Corresponding to project id in XML. 
#   │ 
#   └──subject          --xnatsubjectid        #  --> mapping in MNAP: XNAT_SUBJECT_ID     --> mapping in JSON spec: #SUBJECTID#      --> Corresponding to subject ID in subject-level XML (Subject Accession ID). EXAMPLE in XML        <xnat:subject_ID>BID11_S00192</xnat:subject_ID>
#        │                                                                                                                                                                                                         EXAMPLE in Web UI     Accession number:  A unique XNAT-wide ID for a given human irrespective of project within the XNAT Site
#        │              --xnatsubjectlabel     #  --> mapping in MNAP: XNAT_SUBJECT_LABEL  --> mapping in JSON spec: #SUBJECTLABEL#   --> Corresponding to subject label in subject-level XML (Subject Label).     EXAMPLE in XML        <xnat:field name="SRC_SUBJECT_ID">CU0018</xnat:field>
#        │                                                                                                                                                                                                         EXAMPLE in Web UI     Subject Details:   A unique XNAT project-specific ID that matches the experimenter expectations
#        │ 
#        └──experiment  --xnataccsessionid     #  --> mapping in MNAP: XNAT_ACCSESSION_ID  --> mapping in JSON spec: #ID#             --> Corresponding to subject session ID in session-level XML (Subject Accession ID)   EXAMPLE in XML       <xnat:experiment ID="BID11_E00048" project="embarc_r1_0_0" visit_id="ses-wk2" label="CU0018_MRwk2" xsi:type="xnat:mrSessionData">
#                                                                                                                                                                                                                           EXAMPLE in Web UI    Accession number:  A unique project specific ID for that subject
#                       --xnatsessionlabel     #  --> mapping in MNAP: XNAT_SESSION_LABEL  --> mapping in JSON spec: #LABEL#          --> Corresponding to session label in session-level XML (Session/Experiment Label)    EXAMPLE in XML       <xnat:experiment ID="BID11_E00048" project="embarc_r1_0_0" visit_id="ses-wk2" label="CU0018_MRwk2" xsi:type="xnat:mrSessionData">
#                                                                                                                                                                                                                           EXAMPLE in Web UI    MR Session:   A project-specific, session-specific and subject-specific XNAT variable that defines the precise acquisition / experiment
#
    XNAT_HOST_NAME=`opts_GetOpt "--xnathost" $@`
    XNAT_PROJECT_ID=`opts_GetOpt "--xnatprojectid" $@`
    XNAT_SUBJECT_LABELS=`opts_GetOpt "--xnatsubjectlabels" "$@" | sed 's/,/ /g;s/|/ /g'`; XNAT_SUBJECT_LABELS=`echo "$XNAT_SUBJECT_LABELS" | sed 's/,/ /g;s/|/ /g'`
    XNAT_SESSION_LABELS=`opts_GetOpt "--xnatsessionlabel" "$@" | sed 's/,/ /g;s/|/ /g'`; XNAT_SESSION_LABELS=`echo "$XNAT_SESSION_LABELS" | sed 's/,/ /g;s/|/ /g'`
    if [[ -z ${XNAT_SESSION_LABELS} ]]; then
    XNAT_SESSION_LABELS=`opts_GetOpt "--xnatsessionlabels" "$@" | sed 's/,/ /g;s/|/ /g'`; XNAT_SESSION_LABELS=`echo "$XNAT_SESSION_LABELS" | sed 's/,/ /g;s/|/ /g'`
    fi
    XNAT_SUBJECT_ID=`opts_GetOpt "--xnatsubjectid" $@`
    XNAT_ACCSESSION_ID=`opts_GetOpt "--xnataccsessionid" $@`
    XNAT_USER_NAME=`opts_GetOpt "--xnatuser" $@`
    XNAT_PASSWORD=`opts_GetOpt "--xnatpass" $@`
    XNAT_CREDENTIAL_FILE=`opts_GetOpt "--xnatcredentialfile" $@`
    XNATResetCredentials=`opts_GetOpt "--resetcredentials" $@`
    XNATArchiveCommit=`opts_GetOpt "--xnatarchivecommit" $@`
    XNATgetQC=`opts_GetOpt "--xnatgetqc" $@`
#
# -- END of parsing XNAT arguments

# -- Check acceptance test flag
if [[ -z ${AcceptanceTestSteps} ]]; then 
    usage
    reho "ERROR: --acceptancetest flag not specified. No steps to perform acceptance testing on."; echo "";
    exit 1
else
    # -- Run checks for supported steps
    unset FoundSupported
    echo ""
    geho "--> Checking that requested ${AcceptanceTestSteps} are supported..."
    echo ""
    AcceptanceTestStepsChecks="$AcceptanceTestSteps"
    unset AcceptanceTestSteps
    for AcceptanceTestStep in ${AcceptanceTestStepsChecks}; do
       if [ ! -z "${SupportedAcceptanceTestSteps##*${AcceptanceTestStep}*}" ]; then
           reho "--> ${AcceptanceTestStep} is not supported. Will remove from requested list."
       else
           geho "--> ${AcceptanceTestStep} is supported."
           FoundSupported="yes"
           AcceptanceTestSteps="${AcceptanceTestSteps} ${AcceptanceTestStep}"
       fi
    done
    if [[ -z ${FoundSupported} ]]; then 
        usage
        reho "ERROR: None of the requested acceptance tests are currently supported."; echo "";
        reho "Supported: ${SupportedAcceptanceTestSteps}"; echo "";
        exit 1
    fi
fi

# -- Check and set run type
if [[ -z ${RUN_TYPE} ]]; then 
    RUN_TYPE="local"
    reho "Note: Run type not specified. Setting default turnkey type to local run."; echo ""
    reho "Note: If you wish to run acceptance tests on an XNAT host, re-run with flag --runtype='xnat' "; echo ""
fi

######################## START NON-XNAT SPECIFIC CHECKS  #######################
#
if [[ ${RUN_TYPE} != "xnat" ]]; then 
   if [[ -z ${StudyFolder} ]]; then usage; reho "Error: Requesting local run but --studyfolder flag is missing."; echo ""; exit 1; fi
   if [[ -z ${CASES} ]]; then usage; reho "Error: Requesting local run but --subject flag is missing."; echo ""; exit 1; fi
   if [[ -z ${SESSION_LABELS} ]]; then usage; SESSION_LABELS=""; reho "Note: --sessionlabels are not defined. Assuming no label info."; echo ""; fi
    RunAcceptanceTestDir="${StudyFolder}/processing/logs/acceptTests"
    if [ -z ${SubjectsFolder} ]; then SubjectsFolder="${StudyFolder}/subjects"; fi
    echo ""
    reho "Note: Acceptance tests will be saved in selected study folder: $RunAcceptanceTestOut"
    echo ""
    if [[ ! -d ${RunAcceptanceTestDir} ]]; then mkdir -p ${RunAcceptanceTestDir} > /dev/null 2>&1; fi
fi
#
######################## END NON-XNAT SPECIFIC CHECKS  #########################

########################  START XNAT SPECIFIC CHECKS  ##########################
#
if [[ ${RUN_TYPE} == "xnat" ]]; then
    echo ""
    if [[ -z ${XNAT_PROJECT_ID} ]]; then usage; reho "Error: --xnatprojectid flag missing. Batch parameter file not specified."; echo ''; exit 1; fi
    if [[ -z ${XNAT_HOST_NAME} ]]; then usage; reho "Error: --xnathost flag missing. Batch parameter file not specified."; echo ''; exit 1; fi
    if [[ -z ${XNAT_SESSION_LABELS} ]] && [[ -z ${XNAT_ACCSESSION_ID} ]]; then usage; reho "Error: --xnatsessionlabels and --xnataccsessionid flags are both missing. Please specify session label and re-run."; echo ''; exit 1; fi
    if [[ -z ${XNATArchiveCommit} ]]; then unset XNATArchiveCommit; reho "Note: --xnatarchivecommit not requested. Results will only be stored locally."; echo ''; fi
    if [[  ${XNATArchiveCommit} != "session" &&  ${XNATArchiveCommit} != "project" &&  ${XNATArchiveCommit} != "all" ]]; then reho "Note: --xnatarchivecommit was set to '$XNATArchiveCommit', which is not supported. Check usage for available options."; unset XNATArchiveCommit; echo ''; fi
    if [[ -z ${XNATgetQC} ]]; then unset XNATgetQC; reho "Note: --xnatgetqc not requested. QC images will not be downloaded."; echo ''; fi
    if [[ ${XNATgetQC} != "scene" &&  ${XNATgetQC} != "image" &&  ${XNATgetQC} != "all" &&  ${XNATgetQC} != "png" &&  ${XNATgetQC} != "pngs" &&  ${XNATgetQC} != "images" &&  ${XNATgetQC} != "scenes" &&  ${XNATgetQC} != "snr" &&  ${XNATgetQC} != "SNR" &&  ${XNATgetQC} != "TSNR" &&  ${XNATgetQC} != "SNR" ]]; then 
        reho "Note: --xnatgetqc was set to '$XNATgetQC', which is not supported. Check usage for available options."; unset XNATgetQC; echo ''; 
    fi

    ## -- Check for subject labels
    if [[ -z ${CASES} ]] && [[ -z ${XNAT_SUBJECT_LABELS} ]]; then
        usage
        reho "ERROR: --subjects flag and --xnatsubjectlabels flag not specified. No cases to work with. Please specify either."
        echo ""
        exit 1
    fi
    ## -- Check CASES variable
    if [[ -z ${CASES} ]]; then
        CASES="$XNAT_SUBJECT_LABELS"
        reho "Note: --subjects flag omitted. Assuming specified --xnatsubjectlabels names match the subjects folders on the file system."
        echo ""
    fi
    ## -- Check XNAT_SUBJECT_LABELS
    if [[ -z ${XNAT_SUBJECT_LABELS} ]]; then
        XNAT_SUBJECT_LABELS="$CASES"
        echo ""
        reho "Note: --xnatsubjectlabels flag omitted. Assuming specified --subjects names match the subject labels in XNAT."
        echo ""
    fi

    # ------------------------------------------------------------------------------
    # -- First check if .xnat credentials exist:
    # ------------------------------------------------------------------------------
    
    ## -- Set reseting credentials to no if not provided 
    if [ -z ${XNATResetCredentials} ]; then XNATResetCredentials="no"; fi
    ## -- Set  credentials file name to default if not provided
    if [ -z ${XNAT_CREDENTIAL_FILE} ]; then XNAT_CREDENTIAL_FILE=".xnat"; fi

    ## -- Reset credentials
    if [[ "${ResetCredential}" == "yes" ]]; then
        echo ""
        reho " -- Reseting XNAT credentials in ${HOME}/${XNAT_CREDENTIAL_FILE} "
        rm -f ${HOME}/${XNAT_CREDENTIAL_FILE} &> /dev/null
    fi
    ## -- Check for valid xNAT credential file
    if [ -f ${HOME}/${XNAT_CREDENTIAL_FILE} ]; then
        echo ""
        ceho " -- XNAT credentials in ${HOME}/${XNAT_CREDENTIAL_FILE} found. Performing credential checks... "
        XNAT_USER_NAME=`more ${HOME}/${XNAT_CREDENTIAL_FILE} | cut -d: -f1`
        XNAT_PASSWORD=`more ${HOME}/${XNAT_CREDENTIAL_FILE} | cut -d: -f2`
        if [[ ! -z ${XNAT_USER_NAME} ]] && [[ ! -z ${XNAT_PASSWORD} ]]; then
            echo ""
            ceho " -- XNAT credentials parsed from ${HOME}/${XNAT_CREDENTIAL_FILE} " 
            echo ""
        fi
    else
        echo ""
        reho " -- XNAT credentials in ${HOME}/${XNAT_CREDENTIAL_FILE} NOT found. Checking for --xnatuser and --xnatpass flags."
        echo ""
        if [[ -z ${XNAT_USER_NAME} ]] || [[ -z ${XNAT_PASSWORD} ]]; then
            echo ""
            reho "ERROR: --xnatuser and/or --xnatpass flags are missing. Regenerating credentials now..."
            echo ""
            reho "   --> Enter your XNAT XNAT_HOST_NAME username:"
            if read -s answer; then
                XNAT_USER_NAME=$answer
            fi
            reho "   --> Enter your XNAT XNAT_HOST_NAME password:"
            if read -s answer; then
                XNAT_PASSWORD=$answer
            fi
        else
            echo $XNAT_USER_NAME:$XNAT_PASSWORD >> ${HOME}/${XNAT_CREDENTIAL_FILE}
            chmod 400 ${HOME}/${XNAT_CREDENTIAL_FILE}
            ceho " -- XNAT credentials generated in ${HOME}/${XNAT_CREDENTIAL_FILE}"
            echo ""
        fi
    fi
    ## -- Get credentials
    XNAT_CREDENTIALS=$(cat ${HOME}/${XNAT_CREDENTIAL_FILE})
    CheckXNATConnect=`curl -Is -u ${XNAT_CREDENTIALS} ${XNAT_HOST_NAME} | head -1 | grep "200"`
    if [[ ! -z ${CheckXNATConnect} ]]; then
        ceho " -- XNAT Connection tested OK for ${XNAT_HOST_NAME}. Proceeding..."
        echo ""
        XNAT_USER_NAME=`echo $XNAT_CREDENTIALS | cut -d: -f1`; XNAT_PASSWORD=`echo $XNAT_CREDENTIALS | cut -d: -f2`
    else 
        reho "ERROR: XNAT credentials for ${XNAT_HOST_NAME} failed. Re-check your login and password and your ${HOME}/${XNAT_CREDENTIAL_FILE}"
        echo ""
        exit 1
    fi
    
    ## -- Setup XNAT log variables
    if [[ -z ${StudyFolder} ]]; then
        XNATInfoPath="${HOME}/acceptTests/xnatlogs"
        reho "Note: --subjectsfolder flag omitted. Setting logs to $XNATInfoPath"
        echo ""
    else
        XNATInfoPath="${StudyFolder}/processing/logs/acceptTests/xnatlogs"
    fi
    mkdir -p ${XNATInfoPath} &> /dev/null
    if [[ ! -d ${XNATInfoPath} ]]; then
        echo ""
        reho " -- XNAT info folder ${XNATInfoPath} still not found. Check file system paths or permissions..."
        echo ""
        exit 1
    else
        echo ""
        geho " -- XNAT info folder ${XNATInfoPath} generated. Proceeding..."
        echo ""
    fi
    
    ## -- Setup acceptance test location
    RunAcceptanceTestDir="$(dirname ${XNATInfoPath})"
    if [[ -z ${SubjectsFolder} ]]; then SubjectsFolder="${StudyFolder}/subjects"; fi
    
    echo ""
    reho "Note: Acceptance tests will be saved in selected study folder: $RunAcceptanceTestDir"
    echo ""
    if [[ ! -d ${RunAcceptanceTestDir} ]]; then mkdir -p ${RunAcceptanceTestDir} > /dev/null 2>&1; fi
    
    ## -- Obtain temp info on subjects and experiments in the project
    XNATTimeStamp=`date +%Y-%m-%d_%H.%M.%10N`
    curl -u ${XNAT_USER_NAME}:${XNAT_PASSWORD} -m 30 -X GET "${XNAT_HOST_NAME}/data/subjects?project=${XNAT_PROJECT_ID}&format=csv" > ${XNATInfoPath}/${XNAT_PROJECT_ID}_subjects_${XNATTimeStamp}.csv
    curl -u ${XNAT_USER_NAME}:${XNAT_PASSWORD} -m 30 -X GET "${XNAT_HOST_NAME}/data/experiments?project=${XNAT_PROJECT_ID}&format=csv" > ${XNATInfoPath}/${XNAT_PROJECT_ID}_experiments_${XNATTimeStamp}.csv

    if [ -f ${XNATInfoPath}/${XNAT_PROJECT_ID}_subjects_${XNATTimeStamp}.csv ] && [ -f ${XNATInfoPath}/${XNAT_PROJECT_ID}_experiments_${XNATTimeStamp}.csv ]; then
       echo ""
       geho "  --> Downloaded XNAT project info: "; echo ""
       geho "      ${XNATInfoPath}/${XNAT_PROJECT_ID}_subjects_${XNATTimeStamp}.csv"
       geho "      ${XNATInfoPath}/${XNAT_PROJECT_ID}_experiments_${XNATTimeStamp}.csv"
       echo ""
    else
       if [ ! -f ${XNATInfoPath}/${XNAT_PROJECT_ID}_subjects_${XNATTimeStamp}.csv ]; then
           echo ""
           reho " ERROR: ${XNATInfoPath}/${XNAT_PROJECT_ID}_subjects_${XNATTimeStamp}.csv not found! "
           echo ""
           exit 1
       fi
       if [ ! -f ${XNATInfoPath}/${XNAT_PROJECT_ID}_experiments_${XNATTimeStamp}.csv ]; then
           echo ""
           reho " ERROR: ${XNATInfoPath}/${XNAT_PROJECT_ID}_experiments_${XNATTimeStamp}.csv not found! "
           echo ""
           exit 1
       fi
    fi
fi
#
########################  END XNAT SPECIFIC CHECKS  ############################



# -- Report all requested options
    echo ""
    echo ""
    echo "-- ${scriptName}: Specified Command-Line Options - Start --"
    echo ""
    echo "   MNAP Subjects labels: ${CASES}" 
    if [ "$RUN_TYPE" != "xnat" ]; then
        echo "   MNAP study folder: ${StudyFolder}"
        echo "   MNAP study sessions: ${SESSION_LABELS}"
    fi
    if [ "$RUN_TYPE" == "xnat" ]; then
        echo "   XNAT Hostname: ${XNAT_HOST_NAME}"
        echo "   Reset XNAT site credentials: ${XNATResetCredentials}"
        echo "   XNAT site credentials file: ${HOME}/${XNAT_CREDENTIAL_FILE}"
        echo "   XNAT Project ID: ${XNAT_PROJECT_ID}"
        echo "   XNAT Subject Labels: ${XNAT_SUBJECT_LABELS}"
        if [[ ! -z ${XNAT_SESSION_LABELS} ]]; then 
        echo "   XNAT Session Labels: ${XNAT_SESSION_LABELS}"
        fi
        if [[ ! -z ${XNAT_ACCSESSION_ID} ]]; then 
        echo "   XNAT Accession ID: ${XNAT_ACCSESSION_ID}"
        fi
        echo "   XNAT Archive Commit: ${XNATArchiveCommit}"
        echo "   XNAT get QC images or scenes: ${XNATgetQC}"

    fi
    echo "   MNAP Acceptance test steps: ${AcceptanceTestSteps}"
    if [[ -z ${BOLDS} ]]; then 
        echo "   BOLD runs: ${BOLDS}"
        if [[ -z ${BOLDImages} ]]; then 
            echo "   BOLD Images: ${BOLDImages}"
        fi
    fi
    echo "   MNAP Acceptance test output log: ${RunAcceptanceTestOut}"
    echo ""
    echo "-- ${scriptName}: Specified Command-Line Options - End --"
    echo ""
    geho "------------------------- Start of work --------------------------------"
    echo ""

################################ DO WORK #######################################

main() {

echo ""
ceho "       *****************************************************"
ceho "       ****** Performing MNAP Unit Acceptance Tests ********"
ceho "       *****************************************************"
echo ""

# ------------------------------------------------------------------------------
# -- Check the server you are transfering data from:
# ------------------------------------------------------------------------------

TRANSFERNODE=`hostname`
echo ""
geho "-- Checking data from: ${TRANSFERNODE}"
echo ""

# ------------------------------------------------------------------------------
#  -- Set correct info per subject
# ------------------------------------------------------------------------------

    ## -- Function to run on each subject
    UnitTestingFunction() {
    
            if [ ${RUN_TYPE} == "xnat" ]; then
                XNAT_SUBJECT_LABEL="$CASE"
                unset Status
                # -- Define XNAT_SUBJECT_ID (i.e. Accession number) and XNAT_SESSION_LABEL (i.e. MR Session lablel) for the specific XNAT_SUBJECT_LABEL (i.e. subject)
                unset XNAT_SUBJECT_ID XNAT_SESSION_LABEL_HOST XNAT_ACCSESSION_ID
                XNAT_SUBJECT_ID=`more ${XNATInfoPath}/${XNAT_PROJECT_ID}_subjects_${XNATTimeStamp}.csv | grep "${XNAT_SUBJECT_LABEL}" | awk  -F, '{print $1}'`
                XNAT_SUBJECT_LABEL=`more ${XNATInfoPath}/${XNAT_PROJECT_ID}_subjects_${XNATTimeStamp}.csv | grep "${XNAT_SUBJECT_ID}" | awk  -F, '{print $3}'`
                if [[ -z ${XNAT_SESSION_LABEL} ]]; then
                    XNAT_SESSION_LABEL_HOST=`more ${XNATInfoPath}/${XNAT_PROJECT_ID}_experiments_${XNATTimeStamp}.csv | grep "${XNAT_SUBJECT_LABEL}" | grep "${XNAT_ACCSESSION_ID}" | awk  -F, '{print $5}'`
                    XNAT_SESSION_LABEL=`echo ${XNAT_SESSION_LABEL_HOST} | sed 's|$CASE_||g'`
                else
                    XNAT_SESSION_LABEL_HOST=`more ${XNATInfoPath}/${XNAT_PROJECT_ID}_experiments_${XNATTimeStamp}.csv | grep "${XNAT_SUBJECT_LABEL}" | grep "${XNAT_SESSION_LABEL}" | awk  -F, '{print $5}'`
                fi
                XNAT_ACCSESSION_ID=`more ${XNATInfoPath}/${XNAT_PROJECT_ID}_experiments_${XNATTimeStamp}.csv | grep "${XNAT_SUBJECT_LABEL}" | grep "${XNAT_SESSION_LABEL}" | awk  -F, '{print $1}'`
                
                # -- Report error if variables remain undefined
                if [[ -z ${XNAT_SUBJECT_ID} ]] || [[ -z ${XNAT_SUBJECT_LABEL} ]] || [[ -z ${XNAT_ACCSESSION_ID} ]] || [[ -z ${XNAT_SESSION_LABEL_HOST} ]]; then 
                    echo ""
                    reho "Some or all of XNAT database variables were not set correctly: "
                    echo ""
                    reho "  --> XNAT_SUBJECT_ID     :  $XNAT_SUBJECT_ID "
                    reho "  --> XNAT_SUBJECT_LABEL  :  $XNAT_SUBJECT_LABEL "
                    reho "  --> XNAT_ACCSESSION_ID  :  $XNAT_ACCSESSION_ID "
                    reho "  --> XNAT_SESSION_LABEL  :  $XNAT_SESSION_LABEL_HOST "
                    echo ""
                    Status="FAIL"
                    # -- Set the XNAT_SESSION_LABEL_HOST were it correct to allow naming of the *.txt files
                    XNAT_SESSION_LABEL_HOST="${CASE}_${XNAT_SESSION_LABEL}"
                else
                    echo ""
                    geho "Successfully read all XNAT database variables: "
                    echo ""
                    geho "  --> XNAT_SUBJECT_ID     :  $XNAT_SUBJECT_ID "
                    geho "  --> XNAT_SUBJECT_LABEL  :  $XNAT_SUBJECT_LABEL "
                    geho "  --> XNAT_ACCSESSION_ID  :  $XNAT_ACCSESSION_ID "
                    geho "  --> XNAT_SESSION_LABEL  :  $XNAT_SESSION_LABEL_HOST "
                    echo ""
                fi
            
                # -- Define final variable set
                if [[ ${BIDSFormat} == "yes" ]]; then
                    # -- Setup CASE without the 'MR' prefix in the XNAT_SESSION_LABEL
                    #    Eventually deprecate once fixed in XNAT
                    CASE="${XNAT_SESSION_LABEL_HOST}"
                    CASE=`echo ${CASE} | sed 's|MR||g'`
                    echo " -- Note: --bidsformat='yes' " 
                    echo "    Combining XNAT_SUBJECT_LABEL and XNAT_SESSION_LABEL into unified BIDS-compliant subject variable for MNAP run: ${CASE}"
                    echo ""
                else
                    CASE="${XNAT_SUBJECT_LABEL}"
                fi
            fi
        
            UnitTests=${AcceptanceTestSteps}
            echo ""
            geho "-- Running MNAP unit tests: ${UnitTests}"

            
            ## -- Setup function to check presence of files on either local file system or on XNAT on 
            UnitTestDataCheck() {
                SubjectSessionTimeStamp=`date +%Y-%m-%d_%H.%M.%10N`
                if [[ ${RUN_TYPE} == "xnat" ]]; then
                       if ( curl -k -b "JSESSIONID=$JSESSION" -m 20 -o/dev/null -sfI ${XNAT_HOST_NAME}/data/archive/projects/${XNAT_PROJECT_ID}/subjects/${XNAT_SUBJECT_LABEL}/experiments/${XNAT_SESSION_LABEL_HOST}/resources/mnap_study/files/subjects/${CASE}/${UnitTestData} ); then 
                           Status="PASS"
                           geho "     ${UnitTest} PASS: ${XNAT_HOST_NAME}/data/archive/projects/${XNAT_PROJECT_ID}/subjects/${XNAT_SUBJECT_LABEL}/experiments/${XNAT_SESSION_LABEL_HOST}/resources/mnap_study/files/subjects/${CASE}/${UnitTestData}"
                           echo "  ${UnitTest} PASS: ${XNAT_HOST_NAME}/data/archive/projects/${XNAT_PROJECT_ID}/subjects/${XNAT_SUBJECT_LABEL}/experiments/${XNAT_SESSION_LABEL_HOST}/resources/mnap_study/files/subjects/${CASE}/${UnitTestData}" >> ${RunAcceptanceTestOut}
                           echo "  ${UnitTest} PASS: ${XNAT_HOST_NAME}/data/archive/projects/${XNAT_PROJECT_ID}/subjects/${XNAT_SUBJECT_LABEL}/experiments/${XNAT_SESSION_LABEL_HOST}/resources/mnap_study/files/subjects/${CASE}/${UnitTestData}" >> ${RunAcceptanceTestDir}/${XNAT_SESSION_LABEL_HOST}_${UnitTest}_${SubjectSessionTimeStamp}_${Status}.txt
                           curl -k -b "JSESSIONID=$JSESSION" -s -m 30 -X PUT ${XNAT_HOST_NAME}/data/projects/${XNAT_PROJECT_ID}/subjects/${XNAT_SUBJECT_LABEL}/experiments/${XNAT_SESSION_LABEL_HOST}/resources/${UnitTest}/files/passed.txt?inbody=true -d"pass"
                       else 
                           Status="FAIL"
                           reho "     ${UnitTest} FAIL: ${XNAT_HOST_NAME}/data/archive/projects/${XNAT_PROJECT_ID}/subjects/${XNAT_SUBJECT_LABEL}/experiments/${XNAT_SESSION_LABEL_HOST}/resources/mnap_study/files/subjects/${CASE}/${UnitTestData}"
                           echo "  ${UnitTest} FAIL: ${XNAT_HOST_NAME}/data/archive/projects/${XNAT_PROJECT_ID}/subjects/${XNAT_SUBJECT_LABEL}/experiments/${XNAT_SESSION_LABEL_HOST}/resources/mnap_study/files/subjects/${CASE}/${UnitTestData}" >> ${RunAcceptanceTestOut}
                           echo "  ${UnitTest} FAIL: ${XNAT_HOST_NAME}/data/archive/projects/${XNAT_PROJECT_ID}/subjects/${XNAT_SUBJECT_LABEL}/experiments/${XNAT_SESSION_LABEL_HOST}/resources/mnap_study/files/subjects/${CASE}/${UnitTestData}" >> ${RunAcceptanceTestDir}/${XNAT_SESSION_LABEL_HOST}_${UnitTest}_${SubjectSessionTimeStamp}_${Status}.txt
                       fi
                       if [ -f ${RunAcceptanceTestDir}/${XNAT_SESSION_LABEL_HOST}_${UnitTest}_${SubjectSessionTimeStamp}_${Status}.txt ]; then 
                           echo ""
                           geho "     Individual file saved for XNAT archiving: ${RunAcceptanceTestDir}/${XNAT_SESSION_LABEL_HOST}_${UnitTest}_${SubjectSessionTimeStamp}_${Status}.txt "
                       else
                           echo ""
                           reho "     ERROR: Individual file for XNAT archiving missing: ${RunAcceptanceTestDir}/${XNAT_SESSION_LABEL_HOST}_${UnitTest}_${SubjectSessionTimeStamp}_${Status}.txt "
                       fi
                else
                       if [ -f ${StudyFolder}/subjects/${CASE}/${UnitTestData} ]; then
                           geho "     ${UnitTest} PASS: ${StudyFolder}/subjects/${CASE}/${UnitTestData}"
                           echo "  ${UnitTest} PASS: ${StudyFolder}/subjects/${CASE}/${UnitTestData}" >> ${RunAcceptanceTestOut}
                       else 
                           reho "     ${UnitTest} FAIL: ${StudyFolder}/subjects/${CASE}/${UnitTestData}"
                           echo "  ${UnitTest} FAIL: ${StudyFolder}/subjects/${CASE}/${UnitTestData}" >> ${RunAcceptanceTestOut}
                       fi
                fi
                
                ## -- Get QC data from XNAT
                if [[ ! -z ${XNATgetQC} ]] && [[ ${UnitTest} == "hcp1" ||  ${UnitTest} == "hcp2" ]]; then
                    unset UnitTestQCFolders
                    echo ""
                    reho "     Note: Requested XNAT QC for ${UnitTest} but this is step does not generate QC images."
                    echo ""
                fi
                if [[ ! -z ${XNATgetQC} ]] && [[ ! -z ${UnitTestQCFolders} ]]; then
                    echo ""
                    geho "     Requested XNAT QC ${XNATgetQC} for ${UnitTest}"
                    echo ""
                    if [[ ${XNATgetQC} == "png" ]] || [[ ${XNATgetQC} == "image" ]] || [[ ${XNATgetQC} == "pngs" ]] || [[ ${XNATgetQC} == "images" ]]; then
                        FileTypes="png"
                    fi
                    if [[ ${XNATgetQC} == "scene" ]] || [[ ${XNATgetQC} == "scenes" ]]; then
                        FileTypes="zip"
                    fi
                    if [[ ${XNATgetQC} == "all" ]]; then
                        FileTypes="png zip"
                    fi
                    if [[ ${UnitTest} == "hcp4" ]] || [[ ${UnitTest} == "hcp5" ]]; then
                        FileTypes="${FileTypes} TSNR"
                    fi
                    if [[ ${XNATgetQC} == "snr" ]] || [[ ${XNATgetQC} == "tsnr" ]] || [[ ${XNATgetQC} == "SNR" ]] || [[ ${XNATgetQC} == "TSNR" ]]; then
                        FileTypes="TSNR"
                    fi
                    for UnitTestQCFolder in ${UnitTestQCFolders}; do
                        mkdir -p ${RunAcceptanceTestDir}/QC/${UnitTestQCFolder} > /dev/null 2>&1
                        cd ${RunAcceptanceTestDir}/QC/${UnitTestQCFolder}
                        geho "      --> Working on QC folder $UnitTestQCFolder | Requested QC file types: ${FileTypes}"
                        ceho "          Running: curl -k -b "JSESSIONID=$JSESSION" -s -m 30 -X GET ${XNAT_HOST_NAME}/data/experiments/${XNAT_ACCSESSION_ID}/resources/QC/files/${UnitTestQCFolder}/?format=csv > ${RunAcceptanceTestDir}/QC/${UnitTestQCFolder}/${XNAT_SESSION_LABEL_HOST}_${UnitTest}_${SubjectSessionTimeStamp}_QC_${UnitTestQCFolder}.csv"
                        curl -k -b "JSESSIONID=$JSESSION" -s -m 30 -X GET ${XNAT_HOST_NAME}/data/experiments/${XNAT_ACCSESSION_ID}/resources/QC/files/${UnitTestQCFolder}/?format=csv > ${RunAcceptanceTestDir}/QC/${UnitTestQCFolder}/${XNAT_SESSION_LABEL_HOST}_${UnitTest}_${SubjectSessionTimeStamp}_QC_${UnitTestQCFolder}.csv
                        unset QCFile QCFiles FileType
                        for FileType in ${FileTypes}; do
                            QCFiles=`cat ${XNAT_SESSION_LABEL_HOST}_${UnitTest}_${SubjectSessionTimeStamp}_QC_${UnitTestQCFolder}.csv | sed -e '1,1d' | awk  -F, '{print $1}' | grep "${FileType}"`
                            echo ""
                            for QCFile in ${QCFiles}; do
                                geho "          QC for ${UnitTest} found on XNAT: ${XNAT_HOST_NAME}/data/experiments/${XNAT_ACCSESSION_ID}/resources/QC/files/${UnitTestQCFolder}/${QCFile}"
                                if [[ -f ${RunAcceptanceTestDir}/QC/${UnitTestQCFolder}/${QCFile} ]]; then
                                    geho "          QC for ${UnitTest} found locally: ${RunAcceptanceTestDir}/QC/${UnitTestQCFolder}/${QCFile}"
                                else
                                    curl -k -b "JSESSIONID=$JSESSION" -s -m 30 -X GET "${XNAT_HOST_NAME}/data/experiments/${XNAT_ACCSESSION_ID}/resources/QC/files/${UnitTestQCFolder}/${QCFile}" > ${QCFile}
                                    if [[ -f ${RunAcceptanceTestDir}/QC/${UnitTestQCFolder}/${QCFile} ]]; then
                                        geho "          Results found: ${RunAcceptanceTestDir}/QC/${UnitTestQCFolder}/${QCFile}"
                                    else
                                        reho "          ERROR - results not found: ${RunAcceptanceTestDir}/QC/${UnitTestQCFolder}/${QCFile}"
                                    fi
                                fi
                            done
                            echo ""
                        done
                    done
                    rm ${RunAcceptanceTestDir}/QC/${UnitTestQCFolder}/*.csv > /dev/null 2>&1
                fi
            }
           
            ################## ACCEPTANCE TEST FOR EACH UNIT ###################
            #
            # -- SUPPORTED:
            #    UnitTests="hcp1 hcp2 hcp3 hcp4 hcp5 hcpd FSLDtifit FSLBedpostxGPU preprocessBold computeBOLDfcSeed computeBOLDfcGBC" 
            #
            # -- Needs to be added:
            #    UnitTests="hcpd hcpdLegacy eddyQC FSLDtifit FSLBedpostxGPU pretractographyDense DWIDenseParcellation DWISeedTractography createBOLDBrainMasks computeBOLDStats createStatsReport extractNuisanceSignal preprocessBold preprocessConc g_PlotBoldTS BOLDParcellation computeBOLDfcSeed computeBOLDfcGBC QCPreprocBOLDfc"
            #
            # -- FILES FOR EACH UNIT
            #
            #    hcp1:                       subjects/<session id>/hcp/<session id>/T1w/T1w_acpc_dc_restore_brain.nii.gz
            #    hcp2: FS Version 6.0:       subjects/<session id>/hcp/<session id>/T1w/<session id>/label/BA_exvivo.thresh.ctab
            #    hcp2: FS Version 5.3-HCP:   subjects/<session id>/hcp/<session id>/T1w/<session id>/label/rh.entorhinal_exvivo.label
            #    hcp3:                       subjects/<session id>/hcp/<session id>/T1w/ribbon.nii.gz
            #    hcp4:                       subjects/<session id>/hcp/<session id>/MNINonLinear/Results/<bold code>/<bold code>.nii.gz
            #    hcp5:                       subjects/<session id>/hcp/<session id>/MNINonLinear/Results/<bold code>/<bold code>_Atlas.dtseries.nii
            #    hcpDiffusion:               subjects/<session id>/hcp/<session id>/T1w/Diffusion/data.nii.gz
            #    hcpDTIFix:                  subjects/<session id>/hcp/<session id>/T1w/Diffusion/dti_FA.nii.gz
            #    hcpBedpostx:                subjects/<session id>/hcp/<session id>/T1w/hcpBedpostx/mean_fsumsamples.nii.gz
            #
            # -- To be tested for BOLD processing: 
            #
            #    DenoiseData="Atlas_g7_hpss_res-mVWMWB_lpss.dtseries.nii"
            #    FCData="Atlas_g7_hpss_res-mVWMWB_lpss_BOLD-CAB-NP-v1.0_r.pconn.nii"
            #    BOLDS="1"
            #
            ####################################################################
            
            ## -- Loop over units
            for UnitTest in ${UnitTests}; do
                
                if [ ! -z "${SupportedAcceptanceTestSteps##*${UnitTest}*}" ]; then
                    echo ""
                    reho "  -- ${UnitTest} is not supported. Skipping step for $CASE."
                    echo ""
                else
                    echo ""
                    geho "  -- ${UnitTest} is supported. Proceeding..."
                    echo ""
                    echo "  -- Checking ${UnitTest} for $CASE " >> ${RunAcceptanceTestOut}
                    ## -- Check units that may have multiple bolds
                    if [[ ${UnitTest} == "hcp4" ]] || [[ ${UnitTest} == "hcp5" ]] || [[ ${UnitTest} == "preprocessBold" ]] || [[ ${UnitTest} == "computeBOLDfcSeed" ]] || [[ ${UnitTest} == "computeBOLDfcGBC" ]] || [[ ${UnitTest} == "BOLDImages" ]]; then
                        echo ""
                        if [[ ! -z ${BOLDS} ]]; then
                            for BOLD in ${BOLDS}; do
                                if   [[ ${UnitTest} == "hcp4" ]];           then UnitTestData="hcp/${CASE}/MNINonLinear/Results/${BOLD}/${BOLD}.nii.gz"; UnitTestQCFolders="BOLD"; UnitTestDataCheck
                                elif [[ ${UnitTest} == "hcp5" ]];           then UnitTestData="hcp/${CASE}/MNINonLinear/Results/${BOLD}/${BOLD}_Atlas.dtseries.nii"; UnitTestQCFolders="BOLD"; UnitTestDataCheck
                                elif [[ ${UnitTest} == "preprocessBold" ]]; then UnitTestData="hcp/${CASE}/images/functional/bold${BOLD}_${DenoiseData}"; UnitTestQCFolders="movement"; UnitTestDataCheck
                                elif [[ ${UnitTest} == "computeBOLDfcSeed" ]] || [[ ${UnitTest} == "computeBOLDfcGBC" ]];      then UnitTestData="hcp/${CASE}/images/functional/bold${BOLD}_${FCData}"; UnitTestQCFolders=""; UnitTestDataCheck
                                elif [[ ${UnitTest} == "BOLDImages" ]]; then
                                    for BOLDImage in ${BOLDImages}; do
                                        BOLDImage=`echo ${BOLDImage} | sed "s/{N}/${BOLD}/g"`
                                        UnitTestData="images/functional/${BOLDImage}"; UnitTestQCFolders=""; UnitTestDataCheck
                                    done
                                fi
                            done
                        else
                             echo "  -- Requested ${UnitTest} for ${CASE} but no BOLDS specified." >> ${RunAcceptanceTestOut}
                             echo "" >> ${RunAcceptanceTestOut}
                        fi
                    elif [[ ${UnitTest} == "hcp1" ]];    then UnitTestData="hcp/${CASE}/T1w/T1w_acpc_dc_restore_brain.nii.gz"; UnitTestDataCheck
                    elif [[ ${UnitTest} == "hcp2" ]];    then UnitTestData="hcp/${CASE}/T1w/${CASE}/label/rh.entorhinal_exvivo.label"; UnitTestDataCheck
                    elif [[ ${UnitTest} == "hcp3" ]];    then UnitTestData="hcp/${CASE}/MNINonLinear/ribbon.nii.gz"; UnitTestQCFolders="T1w T2w myelin"; UnitTestDataCheck
                    elif [[ ${UnitTest} == "hcpd" ]]; then UnitTestData="hcp/${CASE}/T1w/Diffusion/data.nii.gz"; UnitTestDataCheck
                    elif [[ ${UnitTest} == "FSLDtifit" ]]; then UnitTestData="hcp/${CASE}/T1w/Diffusion/dti_FA.nii.gz"; UnitTestDataCheck
                    elif [[ ${UnitTest} == "FSLBedpostxGPU" ]]; then UnitTestData="hcp/${CASE}/T1w/Diffusion.bedpostX/mean_fsumsamples.nii.gz"; UnitTestDataCheck
                    fi
                    
                    if [[ ${RUN_TYPE} == "xnat" ]]; then 
                        if [[ ${XNATArchiveCommit} == "session" ]] || [[ ${XNATArchiveCommit} == "all" ]]; then
                            echo ""
                            geho "---> Setting recursive r+w+x permissions on ${RunAcceptanceTestOut}"
                            echo ""
                            chmod -R 777 ${RunAcceptanceTestDir} &> /dev/null
                            cd ${RunAcceptanceTestDir}
                            unset XNATUploadFile
                            XNATUploadFile="${XNAT_SESSION_LABEL_HOST}_${UnitTest}_${SubjectSessionTimeStamp}_${Status}.txt"
                            echo ""
                            geho "---> Uploading ${XNATUploadFile} to ${XNAT_HOST_NAME} "
                            geho "     curl -k -b "JSESSIONID=$JSESSION" -m 40 -X POST "${XNAT_HOST_NAME}/data/archive/projects/${XNAT_PROJECT_ID}/subjects/${XNAT_SUBJECT_LABEL}/experiments/${XNAT_ACCSESSION_ID}/resources/MNAP_ACCEPT/files/${XNATUploadFile}?extract=true&overwrite=true" -F file=@${RunAcceptanceTestDir}/${XNATUploadFile} "
                            echo ""
                            curl -k -b "JSESSIONID=$JSESSION" -m 40 -X POST "${XNAT_HOST_NAME}/data/archive/projects/${XNAT_PROJECT_ID}/subjects/${XNAT_SUBJECT_LABEL}/experiments/${XNAT_ACCSESSION_ID}/resources/MNAP_ACCEPT/files/${XNATUploadFile}?extract=true&overwrite=true" -F file=@${RunAcceptanceTestDir}/${XNATUploadFile} &> /dev/null
                            echo ""
                            if ( curl -k -b "JSESSIONID=$JSESSION" -o/dev/null -sfI ${XNAT_HOST_NAME}/data/archive/projects/${XNAT_PROJECT_ID}/subjects/${XNAT_SUBJECT_LABEL}/experiments/${XNAT_SESSION_LABEL_HOST}/resources/MNAP_ACCEPT/files/${XNATUploadFile} ); then 
                                geho " -- ${XNATUploadFile} uploaded to ${XNAT_HOST_NAME}"
                            else 
                                reho " -- ${XNATUploadFile} not found on ${XNAT_HOST_NAME} Something went wrong with curl."
                            fi
                        fi
                    fi
                fi
            done

    }

    ## -- Loop over subjects    
    if [[ -z ${SESSION_LABELS} ]] && [[ ${RUN_TYPE} != "xnat" ]] ; then
        SESSION_LABELS="_"
    fi
    
    if [[ ${RUN_TYPE} == "xnat" ]]; then
        SESSION_LABELS="${XNAT_SESSION_LABELS}"
    fi
    
    for SESSION_LABEL in ${SESSION_LABELS}; do
    
        if [[ ${RUN_TYPE} == "xnat" ]]; then
            XNAT_SESSION_LABEL="${SESSION_LABEL}"
            ## -- Setup relevant acceptance paths for XNAT run
            unset AcceptDirTimeStamp
            AcceptDirTimeStamp=`date +%Y-%m-%d_%H.%M.%10N`
            RunAcceptanceTestOut="${RunAcceptanceTestDir}/MNAPAcceptanceTest_XNAT_${XNAT_SESSION_LABEL}_${AcceptDirTimeStamp}.txt"
            ## -- Open JSESSION to the XNAT Site
            JSESSION=$(curl -k -X POST -u "${XNAT_CREDENTIALS}" "${XNAT_HOST_NAME}/data/JSESSION" )
            echo ""
            geho "-- JSESSION created: ${JSESSION}"; echo ""
            echo "" >> ${RunAcceptanceTestOut}
            echo "  MNAP Acceptance Test Report for XNAT Run" >> ${RunAcceptanceTestOut}
            echo "  -----------------------------------------" >> ${RunAcceptanceTestOut}
            echo "" >> ${RunAcceptanceTestOut}
            echo "   MNAP Acceptance test steps:    ${AcceptanceTestSteps}" >> ${RunAcceptanceTestOut}
            echo "   XNAT Hostname:                  ${XNAT_HOST_NAME}" >> ${RunAcceptanceTestOut}
            echo "   XNAT Project ID:                ${XNAT_PROJECT_ID}" >> ${RunAcceptanceTestOut}
            echo "   XNAT Session Label:             ${XNAT_SESSION_LABEL}" >> ${RunAcceptanceTestOut}
            echo "" >> ${RunAcceptanceTestOut}
            echo "  ---------------------------" >> ${RunAcceptanceTestOut}
            echo "" >> ${RunAcceptanceTestOut}
        else
            ## -- Setup relevant acceptance paths for non-XNAT run
            unset AcceptDirTimeStamp
            AcceptDirTimeStamp=`date +%Y-%m-%d_%H.%M.%10N`
            RunAcceptanceTestOut="${RunAcceptanceTestDir}/MNAPAcceptanceTest_${AcceptDirTimeStamp}.txt"
            echo "" >> ${RunAcceptanceTestOut}
            echo "  MNAP Acceptance Test Report for Local Run" >> ${RunAcceptanceTestOut}
            echo "  ------------------------------------------" >> ${RunAcceptanceTestOut}
            echo "" >> ${RunAcceptanceTestOut}
            echo "   MNAP Study folder:              ${StudyFolder}" >> ${RunAcceptanceTestOut}
            echo "   MNAP Acceptance test steps:     ${AcceptanceTestSteps}" >> ${RunAcceptanceTestOut}
            echo "" >> ${RunAcceptanceTestOut}
            echo "  ---------------------------" >> ${RunAcceptanceTestOut}
            echo "" >> ${RunAcceptanceTestOut}
        fi
    
        ## -- Execute core function over cases
        for CASE in ${CASES}; do UnitTestingFunction; done
        
        if [[ ${RUN_TYPE} == "xnat" ]]; then
            if [[ ${XNATArchiveCommit} == "all" ]] || [[ ${XNATArchiveCommit} == "project" ]]; then
                 chmod -R 777 ${RunAcceptanceTestDir} &> /dev/null
                 cd ${RunAcceptanceTestDir}
                 RunAcceptanceTestOutFile=$(basename $RunAcceptanceTestOut)
                 echo ""
                 geho "---> Uploading ${RunAcceptanceTestOut} to ${XNAT_HOST_NAME} "
                 geho "     curl -k -b "JSESSIONID=$JSESSION" -m 60 -X POST "${XNAT_HOST_NAME}/data/archive/projects/${XNAT_PROJECT_ID}/resources/MNAP_ACCEPT/files/${RunAcceptanceTestOutFile}?extract=true&overwrite=true" -F file=@${RunAcceptanceTestOut} "
                 echo ""
                 curl -k -b "JSESSIONID=$JSESSION" -m 60 -X POST "${XNAT_HOST_NAME}/data/archive/projects/${XNAT_PROJECT_ID}/resources/MNAP_ACCEPT/files/${RunAcceptanceTestOutFile}?extract=true&overwrite=true" -F file=@${RunAcceptanceTestOut} &> /dev/null
                 echo ""
                 if ( curl -k -b "JSESSIONID=$JSESSION" -m 20 -o/dev/null -sfI ${XNAT_HOST_NAME}/data/archive/projects/${XNAT_PROJECT_ID}/resources/MNAP_ACCEPT/files/${RunAcceptanceTestOutFile} ); then 
                     geho "-- Successfully uploaded ${RunAcceptanceTestOutFile} to ${XNAT_HOST_NAME} under project ${XNAT_PROJECT_ID} as a resource:"
                     geho "                ${XNAT_HOST_NAME}/data/archive/projects/${XNAT_PROJECT_ID}/resources/MNAP_ACCEPT/files/${RunAcceptanceTestOutFile}"
                 else 
                     reho "-- ${RunAcceptanceTestOutFile} not found on ${XNAT_HOST_NAME} Something went wrong with curl."
                 fi
            fi
        fi
        
        ## -- Close JSESSION
        if [[ ${RUN_TYPE} == "xnat" ]]; then
            curl -k -X DELETE -b "JSESSIONID=${JSESSION}" "${XNAT_HOST_NAME}/data/JSESSION"
            echo ""
            geho "-- JSESSION closed: ${JSESSION}"
        fi
        
    done

    echo ""
    ceho "--> Attempted acceptance testing for ${UnitTests} finished."
    echo ""
     if [ -f ${RunAcceptanceTestOut} ]; then
        echo ""
        ceho "--> Final acceptance testing results are stored locally:" 
        ceho "    ${RunAcceptanceTestOut}"
        echo ""
    else 
        echo ""
        reho " ERROR: None of the requested acceptance tests passed: ${UnitTests}"
        reho "        Final results missing:"
        reho "        ${RunAcceptanceTestOut}."
        echo ""
        echo ""
    fi

}

################################ END OF WORK ###################################


# ------------------------------------------------------------------------------
# -- Execute overall function and read arguments
# ------------------------------------------------------------------------------

main $@

# -- Reset sensitive XNAT variables
unset XNAT_USER_NAME XNAT_PASSWORD XNAT_CREDENTIALS XNAT_HOST_NAME &> /dev/null
