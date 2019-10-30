#!/usr/bin/python
import argparse
import os
import re
import shutil
import sys
sys.path.append("/usr/local/bin")

from xnatSession import XnatSession

def get_filename_from_uri(uri):
    return uri.split("/")[-1]

def download_file(uri, local_file):
    xnatSession.renew_httpsession()
    with xnatSession.httpsess.get(url = xnatSession.host + uri, stream = True) as r:
        r.raise_for_status()
        with open(local_file, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

def create_resource(uri):
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.put(xnatSession.host + uri)
    if response.status_code == 409:
        print("Project resource already exists, I will add to it.")
    elif response.status_code != 200:
        raise Exception("Error creating resource %s: %s %s %s" % (uri,
                                                                  response.status_code,
                                                                  response.reason,
                                                                  response.text))
def upload_to_resource(uri, myfile):
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.post(url = xnatSession.host + uri, files = myfile)
    if response.status_code != 200:
        raise Exception("Error uploading %s: %s %s %s" % (uri,
                                                          response.status_code,
                                                          response.reason,
                                                          response.text))


parser = argparse.ArgumentParser(description='Generate script from template by performing string replacement')
parser.add_argument('--templateUri', help='Script template URI', required=True)
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

# Get script template via API
try:
    templateFile = get_filename_from_uri(args.templateUri)
    host = os.environ['XNAT_HOST']
    user = os.environ['XNAT_USER']
    passwd = os.environ['XNAT_PASS']
    if not host or not user or not passwd:
        raise Exception("Host, user, or password not set")
    
    xnatSession = XnatSession(username=user, password=passwd, host=host)
    download_file('/data' + args.templateUri, templateFile)
    
    outputFile = "{}.sh".format(args.sessionId)
    with open(templateFile, 'r') as template, open(outputFile, 'w') as output:
        for s in template:
            string = s.replace("PROJECT_ID", args.projectId) \
                .replace("SUBJECT_ID", args.subjectId) \
                .replace("SUBJECT_LABEL", args.subjectLabel) \
                .replace("SESSION_ID", args.sessionId) \
                .replace("SESSION_LABEL", args.sessionLabel) \
                .replace("USERNAME", user) \
                .replace("PASSWORD", passwd) \
                .replace("HOST", host) \
                .replace("SCANS", scanIdList)
            output.write(string)
 
    print("Generated script %s from template %s" % (outputFile, templateFile))

    # Create resource
    resUrl = '/data/archive/projects/%s/resources/%s-scripts' % (args.projectId, os.path.splitext(templateFile)[0])
    create_resource(resUrl)
    
    # Upload to resource
    url = "%s/files/%s" % (resUrl, outputFile)
    myfile = {'upload': (outputFile, open(outputFile, 'rb'), 'multipart/form-data')}
    upload_to_resource(url, myfile)

finally:
    xnatSession.close_httpsession()
