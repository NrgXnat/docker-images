#!/usr/bin/env python

"""launch-pyradiomics-containers.py

Usage:
    launch-pyradiomics-containers.py HOST USERNAME PASSWORD SESSION PROJECT
    launch-pyradiomics-containers.py (-h | --help)
    launch-pyradiomics-containers.py --version

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

def false_or_empty(l):
    return l is False or len(l) == 0

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

# Find the pyradiomics wrapper ID
print("\nFinding pyradiomics wrapper ID.")
r = s.get(host + '/xapi/commands/available', params={"project": project, "xsiType": "xnat:imageSessionData"})
die_if(not r.ok, message="ERROR: Could not search for available commands.", exit=r.text)

try:
    commandsAvailable = r.json()
except:
    die("ERROR: Improper response from /commands/available", r.text)

pyradiomicsWrapperIds = jsonpath(commandsAvailable, '$[?(@["wrapper-name"] == "pyradiomics-rtstruct")].wrapper-id')
die_if(false_or_empty(pyradiomicsWrapperIds), message="ERROR: Could not find pyradiomics-rtstruct as an available command on project {}.".format(project))

pyradiomicsWrapperId = max(pyradiomicsWrapperIds)
if len(pyradiomicsWrapperIds) > 1:
    print("Found multiple wrapper ids for pyradiomics: {}.\nChoosing max id: {}.".format(pyradiomicsWrapperIds, pyradiomicsWrapperId))
else:
    print("Found pyradiomics wrapper id: {}.".format(pyradiomicsWrapperId))

# Get the launch UI to find all the rt struct masks
print("\nGetting container launch UI for pyradiomics.")
r = s.get(host + '/xapi/projects/{}/wrappers/{}/launch'.format(project, pyradiomicsWrapperId), params={"session": session})
die_if(not r.ok, message="ERROR: Could not get container launch UI.", exit=r.text)

try:
    launchUi = r.json()
except:
    die(message="ERROR: Improper response from /projects/{}/wrappers/{}/launch?session={}".format(project, pyradiomicsWrapperId, session), exit=r.text)

# Do a jsonpath search to find nrrd mask files
print("Searching launch UI to find mask files.")
maskFiles = jsonpath(launchUi, '$.inputs.mask-file.ui.NRRD.values[*].value')

die_if(false_or_empty(maskFiles), message="ERROR: No nrrd mask files found in container launch UI for session {}. Do you need to adjust the matcher?".format(session))

print("Found mask files: {}.".format(maskFiles))

# Launch container with each of the mask files
print("\nBulk launching containers for each of the mask files.")
r = s.post(host + '/xapi/projects/{}/wrappers/{}/bulklaunch'.format(project, pyradiomicsWrapperId),
            json=[{"session": session, "mask-file": maskFile} for maskFile in maskFiles])
die_if(not r.ok, message="ERROR: Launching failed.", exit=r.text)

print("Success!")
