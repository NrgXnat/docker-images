#!/usr/bin/env python
    # -*- coding: utf-8 -*-

"""make-debug-project
Make a debug project. If any already exist, make a new one by incrementing the number.

Usage:
    make-debug-project.py <host> <username> <password> [<project_prefix>]
    make-debug-project.py (-h | --help)
    make-debug-project.py --version

Options:
    -h --help           Show the usage
    --version           Show the version
    <host>              XNAT host
    <username>          XNAT username
    <password>          XNAT password
    <project_prefix>    Name of the project to create. This will be postfixed by "_NN" where N is a digit 0–9. [default: DEBUG_PROJECT]

"""

import sys
import requests
from docopt import docopt
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

version = "1.0"
args = docopt(__doc__, version=version)

host = args['<host>']
username = args['<username>']
password = args['<password>']
project_prefix = args.get('<project_prefix>', 'DEBUG')

s = requests.Session()
s.verify = False
s.auth = (username, password)

print("Requesting project list from {}.".format(host))
r = s.get(host + '/data/projects')
if not r.ok:
    sys.exit("ERROR {}: {}".format(r.status_code, r.text))

try:
    raw_result = r.json()
except ValueError:
    sys.exit("ERROR: Could not intepret server response as JSON.\n{}".format(r.text))

try:
    project_object_list = raw_result["ResultSet"]["Result"]
except KeyError:
    sys.exit("ERROR: Server response did not have required {\"ResultSet\": {\"Result\": \{...\}} structure.\n{}".format(r.text))

project_list = [proj["ID"] for proj in project_object_list]

print("Found project list. Searching for pre-existing projects with prefix \"{}\".".format(project_prefix))

for project_index in xrange(101):
    if project_index == 100:
        sys.exit("ERROR: All 100 debug projects with prefix {} already exist. Remove some projects or choose a new debug prefix.".format(project_prefix))
    project_name = "{}_{:02d}".format(project_prefix, project_index)
    if project_name in project_list:
        print("Project {} already exists.".format(project_name))
        continue
    else:
        print("Project {} does not exist.".format(project_name))
        break

print("Creating project {}.".format(project_name))
project_create_params = {"ID": project_name, "secondary_ID": project_name, "name": project_name}
r = s.post(host + '/data/projects', params=project_create_params)
if not r.ok:
    sys.exit("ERROR {}: {}".format(r.status_code, r.text))

print("Project {} created.".format(project_name))
print("Done")