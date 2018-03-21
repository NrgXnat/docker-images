#!/usr/bin/env python

from lxml.builder import ElementMaker
from lxml.etree import tostring as xmltostring
import datetime as dt
import sys
import json
import argparse
import requests

versionNumber='1'
dateString='20180321'
author='flavin'
progName=sys.argv[0].split('/')[-1]
idstring = '$Id: %s,v %s %s %s Exp $'%(progName,versionNumber,dateString,author)

nsdict = {'xnat':'http://nrg.wustl.edu/xnat',
          'xsi':'http://www.w3.org/2001/XMLSchema-instance'}
def ns(namespace, tag):
    return "{%s}%s" % (nsdict[namespace], tag)

def schemaLoc(namespace):
    return "{0} https://www.xnat.org/schemas/{1}/{1}.xsd".format(nsdict[namespace], namespace)

def generateScanDict(scanId):
    return {
        "imageScan_ID": scanId,
        "coverage": "0",
        "motion": "0",
        "otherImageArtifacts": "0",
        "pass": "1"
    }

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
    parser.add_argument('scansCsv', help='Comma-separated list of scan ids. Will generate random QC info for each.')
    parser.add_argument('outpath',
                        help='Path to XML assessor file (output)')
    args=parser.parse_args()
    #######################################################

    #######################################################
    # GENERATE RANDOM USER
    r = requests.get('https://randomuser.me/api/')
    if r.ok:
        userResults = r.json()['results'][0]
        nameObj = userResults['name']
        name = ' '.join((nameObj['title'], nameObj['first'], nameObj['last']))
    else:
        name = 'A. User'
    #######################################################

    #######################################################
    # ASSEMBLE HEADERS AND OTHER NECESSARY INFO
    sessionId = args.sessionId
    sessionLabel = args.sessionLabel
    project = args.project
    scans = args.scansCsv.split(',')
    outpath = args.outpath

    now = dt.datetime.today()
    isodate = now.strftime('%Y-%m-%d')
    datestamp = now.strftime('%Y%m%d%H%M%S')

    assessorId = '{}_qc_{}'.format(sessionId, datestamp)
    assessorLabel = '{}_qc_{}'.format(sessionLabel, datestamp)

    assessorElementsDict = {
        "date": isodate,
        "imageSession_ID": sessionId,
        "rater": name,
        "stereotacticMarker": "0",
        "incidentalFindings": "None",
        "comments": "Looks good",
        "pass": "1",
        "payable": "1",
        "rescan": "0"
    }

    assessorTitleAttributesDict = {
        'ID': assessorId,
        'project': project,
        'label': assessorLabel,
        ns('xsi','schemaLocation'): schemaLoc('xnat')
    }

    scanDicts = [generateScanDict(scanId) for scanId in scans]
    #######################################################

    #######################################################
    # BUILD ASSESSOR XML
    # Building XML using lxml ElementMaker.
    # For documentation, see http://lxml.de/tutorial.html#the-e-factory
    E = ElementMaker(namespace=nsdict['xnat'], nsmap=nsdict)
    assessorXML = E('QCManualAssessment', assessorTitleAttributesDict,
        E('scans',
            *[E('scan',
                *[E(name, value) for name, value in scanDict.iteritems()])
            for scanDict in scanDicts]),
        *[E(name, value) for name, value in assessorElementsDict.iteritems()]
    )

    print 'Writing assessor XML to %s' % outpath
    # print(xmltostring(assessorXML, pretty_print=True))
    with open(outpath, 'w') as f:
        f.write(xmltostring(assessorXML, pretty_print=True, encoding='UTF-8', xml_declaration=True))

if __name__ == '__main__':
    print idstring
    main()
