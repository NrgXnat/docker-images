#!/bin/bash

while getopts "p:s:e:b:i:t:" options; do
    case $options in
        p ) echo "XNAT project: $OPTARG"
            project=$OPTARG;;
        s ) echo "XNAT subject: $OPTARG"
            subject=$OPTARG;;
        e ) echo "XNAT session: $OPTARG"
            session=$OPTARG;;
        b ) echo "Bold list: $OPTARG"
            boldList=$OPTARG;;
        i ) echo "Bold images: $OPTARG"
            boldImages=$OPTARG;;
        t ) echo "Acceptance tests: $OPTARG"
            tests=$OPTARG;;
        \?) echo "Unknown option"
            exit 1;;
    esac
done

if [[ $XNAT_HOST =~ localhost ]]; then
    XNAT_HOST=${XNAT_HOST/localhost/host.docker.internal}
fi

boldImageArg=${boldImages:+"--boldimages=$boldImages"}

MNAPAcceptanceTest.sh --xnathost="$XNAT_HOST" --xnatuser="$XNAT_USER" --xnatpass="$XNAT_PASS" \
    --bidsformat="yes" --runtype="xnat" --xnatarchivecommit="session" \
    --xnatprojectid="$project" --subjects="$subject" --xnatsessionlabels=$session \
    --bolds="$boldList" --acceptancetest="$tests" $boldImageArg

result=$?
echo "Exiting with status $result"
exit $result
