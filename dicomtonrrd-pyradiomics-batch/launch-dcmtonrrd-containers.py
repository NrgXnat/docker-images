#!/usr/bin/env python

"""launch-dcmtonrrd-containers.py

Usage:
    launch-dcmtonrrd-containers.py HOST USERNAME PASSWORD SESSION PROJECT
    launch-dcmtonrrd-containers.py (-h | --help)
    launch-dcmtonrrd-containers.py --version

Options:
    -h --help           Show the usage
    --version           Show the version
    HOST                URL of XNAT server
    USERNAME            Username (or "alias" value from an alias token)
    PASSWORD            Password (or "secret" value from an alias token)
    SESSION             Session ID
    PROJECT             Project name
"""

import requests
from docopt import docopt
from jsonpath import jsonpath

def die_if(condition, message="ERROR", exit=1):
    if condition:
        die(message=message, exit=exit)

def die(message="ERROR", exit=1):
    import sys
    print(message)
    sys.exit(exit)

version = "1.0"

args = docopt(__doc__, version=version)

host     = args.get('HOST')
username = args.get('USERNAME')
password = args.get('PASSWORD')
session  = args.get('SESSION')
project  = args.get('PROJECT')

s = requests.Session()
s.auth = (username, password)

print("Attempting to connect to XNAT at {}.".format(host))
r = s.get(host + "/data/JSESSION")
die_if(not r.ok, message="ERROR: Connection failed.", exit=r.text)
print("OK")

# Find the dcmtonrrd wrapper ID
print("\nFinding dcmtonrrd wrapper ID.")
r = s.get(host + '/xapi/commands/available', params={"project": project, "xsiType": "xnat:imageScanData"})
die_if(not r.ok, message="ERROR: Could not search for available commands.", exit=r.text)

try:
    commandsAvailable = r.json()
except:
    die("ERROR: Improper response from /commands/available", r.text)

dcmtonrrdWrapperId = 0
dcmtonrrdRtstructWrapperId = 0
for commandAvailable in commandsAvailable:
    if commandAvailable["wrapper-name"] == "dicomtonrrd-scan":
        if dcmtonrrdWrapperId == 0:
            dcmtonrrdWrapperId = commandAvailable["wrapper-id"]
            print("Found dcmtonrrd wrapper ID: {}.".format(dcmtonrrdWrapperId))
        else:
            anotherDcmtonrrdWrapperId = commandAvailable["wrapper-id"]
            dcmtonrrdWrapperId = max(dcmtonrrdWrapperId, anotherDcmtonrrdWrapperId)

            print("Found another dcmtonrrd wrapper ID: {}. Keeping max ID: {}.".format(anotherDcmtonrrdWrapperId, dcmtonrrdWrapperId))
    elif commandAvailable["wrapper-name"] == "dicomtonrrd-rtstruct-scan":
        if dcmtonrrdRtstructWrapperId == 0:
            dcmtonrrdRtstructWrapperId = commandAvailable["wrapper-id"]
            print("Found dcmtonrrd-rtstruct wrapper ID: {}.".format(dcmtonrrdRtstructWrapperId))
        else:
            anotherDcmtonrrdRtstructWrapperId = commandAvailable["wrapper-id"]
            dcmtonrrdRtstructWrapperId = max(dcmtonrrdRtstructWrapperId, anotherDcmtonrrdRtstructWrapperId)

            print("Found another dcmtonrrd-rtstruct wrapper ID: {}. Keeping max ID: {}.".format(anotherDcmtonrrdRtstructWrapperId, dcmtonrrdRtstructWrapperId))


die_if(dcmtonrrdWrapperId == 0, message="ERROR: Could not find dcmtonrrd as an available command on project {}.".format(project))
die_if(dcmtonrrdRtstructWrapperId == 0, message="ERROR: Could not find dcmtonrrd-rtstruct as an available command on project {}.".format(project))



print("\nGetting session " + session)
r = s.get(host + '/data/experiments/' + session, params={"format": "json"})
die_if(not r.ok, message="ERROR: Could not get session.", exit=r.text)

try:
    sessionJson = r.json()
except:
    die(message="ERROR: Improper response from /data/experiments/{}".format(session), exit=r.text)

# Do a jsonpath search to find scan
print("Searching session json to find scans.")
imageScans = jsonpath(sessionJson, '$.items[0].children[?(@.field == "scans/scan")].items[?(@.data_fields.modality != "RTSTRUCT")].data_fields.ID')
rtstructScans = jsonpath(sessionJson, '$.items[0].children[?(@.field == "scans/scan")].items[?(@.data_fields.modality == "RTSTRUCT")].data_fields.ID')

die_if(imageScans == False, message='No image scans found.', exit=sessionJson)
die_if(rtstructScans == False, message='No rtstruct scans found.', exit=sessionJson)

print("Found image scans: [{}].".format(", ".join(imageScans)))
print("Found rtstruct scans: [{}].".format(", ".join(rtstructScans)))

# Launch container with each of the scans
print("\nBulk launching containers for each of the image scans.")
launchArgs = [{"scan": '/experiments/' + session + '/scans/' + scan} for scan in imageScans]
r = s.post(host + '/xapi/projects/{}/wrappers/{}/bulklaunch'.format(project, dcmtonrrdWrapperId), json=launchArgs)
die_if(not r.ok, message="ERROR: Launching failed.", exit=r.text)

print("\nBulk launching containers for each of the rtstruct scans.")
launchArgs = [{"scan": '/experiments/' + session + '/scans/' + scan} for scan in rtstructScans]
r = s.post(host + '/xapi/projects/{}/wrappers/{}/bulklaunch'.format(project, dcmtonrrdRtstructWrapperId), json=launchArgs)
die_if(not r.ok, message="ERROR: Launching failed.", exit=r.text)

print("Success!")
