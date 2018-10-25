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

import sys
import requests
from docopt import docopt
from jsonpath import jsonpath

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
if not r.ok:
    print("ERROR: Connection failed.")
    sys.exit(r.text)
print("OK")

# Find the pyradiomics wrapper ID
print("\nFinding pyradiomics wrapper ID.")
r = s.get(host + '/xapi/commands/available', params={"project": project, "xsiType": "xnat:imageSessionData"})
if not r.ok:
    print("ERROR: Could not search for available commands.")
    sys.exit(r.text)

try:
    commandsAvailable = r.json()
except:
    print("ERROR: Improper response from /commands/available")
    sys.exit(r.text)

pyradiomicsWrapperId = 0
for commandAvailable in commandsAvailable:
    if commandAvailable["wrapper-name"] == "pyradiomics-rtstruct":
        if pyradiomicsWrapperId == 0:
            pyradiomicsWrapperId = commandAvailable["wrapper-id"]
            print("Found pyradiomics wrapper ID: {}.".format(pyradiomicsWrapperId))
        else:
            anotherPyradiomicsWrapperId = commandAvailable["wrapper-id"]
            pyradiomicsWrapperId = max(pyradiomicsWrapperId, anotherPyradiomicsWrapperId)

            print("Found another pyradiomics wrapper ID: {}. Keeping max ID: {}.".format(anotherPyradiomicsWrapperId, pyradiomicsWrapperId))

if pyradiomicsWrapperId == 0:
    print("ERROR: Could not find pyradiomics-rtstruct as an available command on project {}.".format(project))
    sys.exit(1)

# Get the launch UI to find all the rt struct masks
print("\nGetting container launch UI for pyradiomics.")
r = s.get(host + '/xapi/projects/{}/wrappers/{}/launch'.format(project, pyradiomicsWrapperId), params={"session": session})
if not r.ok:
    print("ERROR: Could not get container launch UI.")
    sys.exit(r.text)

try:
    launchUi = r.json()
except:
    print("ERROR: Improper response from /projects/{}/wrappers/{}/launch?session={}".format(project, pyradiomicsWrapperId, session))
    sys.exit(r.text)

# Do a jsonpath search to find nrrd mask files
print("Searching launch UI to find mask files.")
maskFiles = jsonpath(launchUi, '$.input-values[?(@.name == "session")].values[0].children[?(@.name == "mask-scan")].values[0].children[?(@.name == "mask-resource")].values[0].children[?(@.name == "mask-file")].values[*].value')

if maskFiles is False:
    print("ERROR: No nrrd mask files found in container launch UI for session {}. Do you need to adjust the matcher?".format(session))
    sys.exit(1)

print("Found mask files: [{}].".format(", ".join(maskFiles)))

# Launch container with each of the mask files
print("\nBulk launching containers for each of the mask files.")
launchArgs = [{"session": session, "mask-file": maskFile} for maskFile in maskFiles]
r = s.post(host + '/xapi/projects/{}/wrappers/{}/bulklaunch'.format(project, pyradiomicsWrapperId), json=launchArgs)

if not r.ok:
    print("ERROR: Launching failed.")
    sys.exit(r.text)

print("Success!")
