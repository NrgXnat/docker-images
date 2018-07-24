#!/usr/bin/env python

from lxml.builder import ElementMaker
from lxml.etree import tostring as xmltostring
import datetime as dt
import sys
import json
import random
import argparse
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

versionNumber='1.1'
dateString='20180724'
author='flavin'
progName=sys.argv[0].split('/')[-1]
idstring = '$Id: %s,v %s %s %s Exp $'%(progName,versionNumber,dateString,author)

nsdict = {'xnat':'http://nrg.wustl.edu/xnat',
          'xsi':'http://www.w3.org/2001/XMLSchema-instance'}
def ns(namespace, tag):
    return "{%s}%s" % (nsdict[namespace], tag)

def schemaLoc(namespace):
    return "{0} https://www.xnat.org/schemas/{1}/{1}.xsd".format(nsdict[namespace], namespace)

def main():
    #######################################################
    # PARSE INPUT ARGS
    parser = argparse.ArgumentParser(description='Generate XML assessor file from PUP output logs')
    parser.add_argument('-v', '--version',
                        help='Print version number and exit',
                        action='version',
                        version=versionNumber)
    parser.add_argument('--idstring',
                        help='Print id string and exit',
                        action='version',
                        version=idstring)
    parser.add_argument('sessionId', help='Session id')
    parser.add_argument('sessionLabel', help='Session label')
    parser.add_argument('project', help='Project')
    parser.add_argument('xnat_host', help='XNAT Host')
    parser.add_argument('xnat_user', help='XNAT Username')
    parser.add_argument('xnat_pass', help='XNAT Password')
    parser.add_argument('outpath',
                        help='Path to XML assessor file (output)')
    args=parser.parse_args()
    #######################################################

    #######################################################
    # ASSEMBLE HEADERS AND OTHER NECESSARY INFO
    print("Parsing input arguments")
    sessionId = args.sessionId
    sessionLabel = args.sessionLabel
    project = args.project
    # scans = args.scansCsv.split(',')
    outpath = args.outpath

    xnat_host = args.xnat_host
    xnat_user = args.xnat_user
    xnat_pass = args.xnat_pass

    now = dt.datetime.today()
    isodate = now.strftime('%Y-%m-%d')
    datestamp = now.strftime('%Y%m%d%H%M%S')

    assessorId = '{}_qc_{}'.format(sessionId, datestamp)
    assessorLabel = '{}_qc_{}'.format(sessionLabel, datestamp)
    #######################################################

    #######################################################
    # GET LIST OF SCANS ON SESSION
    print("Getting list of scans for session {} (id {}) on XNAT {}.".format(sessionLabel, sessionId, xnat_host))
    s = requests.Session()
    s.verify = False
    s.auth = (xnat_user, xnat_pass)

    r = s.get(xnat_host + '/data/JSESSION')
    if not r.ok:
        print("ERROR Could not connect to XNAT host {}.".format(xnat_host))
        sys.exit(r.text)

    r = s.get(xnat_host + '/data/experiments/{}/scans'.format(sessionId))
    if not r.ok:
        print("ERROR Could not get scans from XNAT host {}, experiment {}.".format(xnat_host, sessionId))
        sys.exit(r.text)

    scans = [scan['ID'] for scan in r.json().get('ResultSet', {}).get('Result', []) if 'ID' in scan]
    print("Got scans {}.".format(scans))
    #######################################################

    #######################################################
    # GENERATE RANDOM USER
    print("Generating random user information.")
    r = requests.get('https://randomuser.me/api/', params={"inc": "name", "noinfo": "true", "nat": "us"})
    if r.ok:
        userResults = r.json()['results'][0]
        nameObj = userResults['name']
        name = ' '.join((nameObj['title'], nameObj['first'], nameObj['last']))
    else:
        name = 'A. User'
    print("Generated username {}.".format(name))
    #######################################################

    #######################################################
    # BUILD ASSESSOR XML
    # Building XML using lxml ElementMaker.
    # For documentation, see http://lxml.de/tutorial.html#the-e-factory

    print("Constructing assessor XML.")
    E = ElementMaker(namespace=nsdict['xnat'], nsmap=nsdict)

    assessorTitleAttributesDict = {
        'ID': assessorId,
        'project': project,
        'label': assessorLabel,
        ns('xsi','schemaLocation'): schemaLoc('xnat')
    }

    assessorElementsList = [
        E("date", isodate),
        E("imageSession_ID", sessionId),
        E("rater", name),
        E("stereotacticMarker", random.choice(["0", "1"])),
        E("incidentalFindings", random.choice(["None", "There is something here", "Wowza!", "Nothing", "Nada", "Bupkis", "Meh"])),
        E("scans",
            *[E("scan",
                E("imageScan_ID", scanId),
                E("coverage", random.choice(["0", "1", "0.5", "0.25", "0.75", "0.9", "0.1"])),
                E("motion", random.choice(["0", "1", "0.5", "0.25", "0.75", "0.9", "0.1"])),
                E("otherImageArtifacts", random.choice(["None", "NA", "none", "Nothing", "Blurry pixels", "Obscured obscura", "Smudge on the lens", "No", "Nope", "Nothing"])),
                E("pass", random.choice(["1", "0", "Yes", "No"]))
            ) for scanId in scans]
        ),
        E("comments", random.choice(["Looks good", "All good", "Good", "Bad", "None", "NA"])),
        E("pass", random.choice(["1", "0", "Yes", "No"])),
        E("payable", random.choice(["1", "0", "Yes", "No"])),
        E("rescan", random.choice(["1", "0", "Yes", "No"]))
    ]

    assessorXML = E('QCManualAssessment', assessorTitleAttributesDict, *assessorElementsList)

    print('Writing assessor XML to {}'.format(outpath))
    # print(xmltostring(assessorXML, pretty_print=True))
    with open(outpath, 'w') as f:
        f.write(xmltostring(assessorXML, pretty_print=True, encoding='UTF-8', xml_declaration=True))

if __name__ == '__main__':
    print idstring
    main()
