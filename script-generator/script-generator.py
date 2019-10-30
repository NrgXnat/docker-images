#!/usr/bin/python
import argparse
import os

parser = argparse.ArgumentParser(description='Generate script from template by performing string replacement')
parser.add_argument('--host', help='XNAT host', required=True)
parser.add_argument('--user', help='XNAT user', required=True)
parser.add_argument('--passwd', help='XNAT pass', required=True)
parser.add_argument('--template', help='Script template', required=True)
parser.add_argument('--outputDir', help='Output directory', required=True)
parser.add_argument('--projectId', help='XNAT project ID', required=True)
parser.add_argument('--subjectId', help='XNAT subject ID', required=True)
parser.add_argument('--subjectLabel', help='XNAT subject label', required=True)
parser.add_argument('--sessionId', help='XNAT session ID', required=True)
parser.add_argument('--sessionLabel', help='XNAT session ID', required=True)
parser.add_argument('--scanIds', help='XNAT scan IDs (comma separated)')

args = parser.parse_args()

# Handle optional scans
if args.scanIds is not None:
    scanIdList = args.scanIds.replace(",", " ")
else:
    scanIdList = ""

outputFile = os.path.join(args.outputDir, "{}.sh".format(args.sessionId))
with open(args.template, 'r') as template, open(outputFile, 'w') as output:
    for s in template:
        string = s.replace("PROJECT_ID", args.projectId) \
            .replace("SUBJECT_ID", args.subjectId) \
            .replace("SUBJECT_LABEL", args.subjectLabel) \
            .replace("SESSION_ID", args.sessionId) \
            .replace("SESSION_LABEL", args.sessionLabel) \
            .replace("USERNAME", args.user) \
            .replace("PASSWORD", args.passwd) \
            .replace("HOST", args.host) \
            .replace("SCANS", scanIdList)
        output.write(string)
