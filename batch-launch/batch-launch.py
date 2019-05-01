#!/usr/bin/env python

"""batch-launch.py

Usage:
    batch-launch.py (scans|sessions|subjects) HOST USERNAME PASSWORD WRAPPER_NAME PARENT_ID PROJECT
    batch-launch.py (-h | --help)
    batch-launch.py --version

Options:
    -h --help           Show the usage
    --version           Show the version
    HOST                URL of XNAT server
    USERNAME            Username (or "alias" value from an alias token)
    PASSWORD            Password (or "secret" value from an alias token)
    WRAPPER_NAME        Name of the wrapper to launch.
    PARENT_ID           ID of parent object. (For instance, when looping on scans, PARENT_ID is a session ID.)
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

host        = args.get('HOST')
username    = args.get('USERNAME')
password    = args.get('PASSWORD')
wrapperName = args.get("WRAPPER_NAME")
parentId    = args.get('PARENT_ID')
project     = args.get('PROJECT')

if args.get("scans"):
    thingString = "scans"
    xsiType = "xnat:imageScanData"
    searchUriTemplate = "/data/experiments/{}/scans"
    jsonpathSearch = '$.ResultSet.Result[*].ID'
    launchArgTemplate = "/experiments/{}".format(parentId) + "/scans/{}"
elif args.get("sessions"):
    thingString = "sessions"
    xsiType = "xnat:imageSessionData"
    searchUriTemplate = "/data/subjects/{}/experiments"
    jsonpathSearch = '$.items[0].children[?(@.field == "experiments/experiment")].items[*].data_fields.ID'
    launchArgTemplate = "{}"
elif args.get("subjects"):
    thingString = "subjects"
    xsiType = "xnat:subjectData"
    searchUriTemplate = "/data/projects/{}/subjects"
    jsonpathSearch = "$.ResultSet.Result[*].ID"
    launchArgTemplate = "{}"
else:
    die("ERROR: Please run batch-launch.py with the first argument being \"scans\", \"sessions\", or \"subjects\".", exit=__doc__)

searchUri = searchUriTemplate.format(parentId)

s = requests.Session()
s.auth = (username, password)

print("Attempting to connect to XNAT at {}.".format(host))
r = s.get(host + "/data/JSESSION")
die_if(not r.ok, message="ERROR: Connection failed.", exit=r.text)
print("OK")

# Find the wrapper ID
print("\nFinding {} wrapper ID.".format(wrapperName))
r = s.get(host + '/xapi/commands/available', params={"project": project, "xsiType": xsiType})
die_if(not r.ok, message="ERROR: Could not search for available commands.", exit=r.text)

try:
    commandsAvailable = r.json()
except:
    die("ERROR: Improper response from /commands/available", r.text)

wrapperIds = jsonpath(commandsAvailable, '$[?(@["wrapper-name"] == "{}" && @.enabled)].wrapper-id'.format(wrapperName))
die_if(false_or_empty(wrapperIds), message="ERROR: Could not find {} as an enabled command on project {}.".format(wrapperName, project))

wrapperId = max(wrapperIds)
if len(wrapperIds) > 1:
    print("Found multiple wrapper ids: {}.\nChoosing max id: {}.".format(wrapperIds, wrapperId))
else:
    print("Found wrapper id: {}.".format(wrapperId))

print("\nFinding root element name for wrapper ID {}.".format(wrapperId))
rootElementNameList = jsonpath(commandsAvailable, '$[?(@["wrapper-id"] == {})].root-element-name'.format(wrapperId))
die_if(false_or_empty(rootElementNameList), message="ERROR: Could not find root-element-name for wrapper-id {} in /commands/available.".format(wrapperId))
die_if(len(rootElementNameList) > 1, message="ERROR: Could not find unique root-element-name for wrapper-id {} in /commands/available.".format(wrapperId))
rootElementName = rootElementNameList[0]

print("\nSearching for {} with URI {}.".format(thingString, searchUri))
r = s.get(host + searchUri, params={"format": "json"})
die_if(not r.ok, message="ERROR: Search failed.", exit=r.text)

try:
    searchJson = r.json()
except:
    die(message="ERROR: Improper response from {}".format(searchUri), exit=r.text)

# Do a jsonpath search to find scan
print("Searching json to find {}.".format(thingString))
results = jsonpath(searchJson, jsonpathSearch)

die_if(results == False, message='No {} found.'.format(thingString), exit=searchJson)

print("Found {}: {}.".format(thingString, results))

# Launch container with each of the things
print("\nBulk launching {} containers for each of the {}.".format(wrapperName, thingString))
launchArgs = [{rootElementName: launchArgTemplate.format(thing)} for thing in results]
url = host + '/xapi/projects/{}/wrappers/{}/bulklaunch'.format(project, wrapperId)
r = s.post(url, json=launchArgs, timeout=None)
die_if(not r.ok, message='ERROR: Batch launch failed. POST to URL {} returned status {}. Args: {}'.format(url, r.status_code, launchArgs), exit=r.text)

try:
    launchReport = r.json()
    successes = launchReport.get("successes", [])
    failures = launchReport.get("failures", [])
    atLeastOneSuccess = len(successes) > 0
    atLeastOneFailure = len(failures) > 0

    if atLeastOneSuccess:
        if atLeastOneFailure:
            print("SUCCESSFUL LAUNCHES")
        else:
            print("ALL LAUNCHES SUCCEEDED!")

        print(rootElementName + " - container id")
        for success in successes:
            print("{} - {}".format(success.get("params", {}).get(rootElementName), success.get("container-id")))

    if atLeastOneFailure:
        if atLeastOneSuccess:
            print("FAILED LAUNCHES")
        else:
            print("ALL LAUNCHES FAILED!")

        print(rootElementName + " - error message")
        for failure in failures:
            print("{} - \"{}\"".format(failure.get("params", {}).get(rootElementName), failure.get("message")))

except:
    print("Could not parse launch report.\n" + r.text)

