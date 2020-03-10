#!/usr/bin/env python

"""bids2xnat
Turn files in BIDS format into XNAT archive format.

Usage:
    bids2xnat.py <inputDir> <outputDir>
    bids2xnat.py (-h | --help)
    bids2xnat.py --version

Options:
    -h --help           Show the usage
    --version           Show the version
    <inputDir>          Directory with BIDS-formatted files.
    <outputDir>         Directory in which BIDS formatted files session-level files will be written
"""

import os
import sys
import json
import shutil
import csv
import tempfile
import zipfile
import traceback
from glob import glob
from docopt import docopt
from xnatjsession import XnatSession

resMap = {}
resMap['NIFTI'] = {'format': 'NIFTI', 'content': 'NIFTI_RAW', 'tags': 'BIDS', 'extract': True}
resMap['BIDS']  = {'format': 'BIDS', 'content': 'BIDS', 'tags': 'BIDS', 'extract': True}

def parseAndUpload(tsvfile):
    sesDir = os.path.dirname(tsvfile)
    sessionId = None
    scansAndFiles = {}
    with open(tsvfile, 'r') as tsv:
        reader = csv.DictReader(tsv, delimiter='\t')
        for row in reader:
            if sessionId is None:
                sessionId = row['xnat_session_id']
            elif sessionId != row['xnat_session_id']:
                raise Exception('{} has a mix of xnat_session_ids, unsure what to do'.format(tsvfile))
            scanId = row['xnat_scan_id']
            if scanId not in scansAndFiles.keys():
                scansAndFiles[scanId] = {}
                scansAndFiles[scanId]['NIFTI'] = []
                scansAndFiles[scanId]['BIDS'] = []
            niftis = glob(os.path.join(sesDir, row['filename'] + '.nii*'))
            bidsjson = os.path.join(sesDir, row['filename'] + '.json')
            if len(niftis) == 0 or not os.path.isfile(bidsjson):
                raise Exception('Missing nifti and/or json for {}'.format(row['filename']))
            elif len(niftis) > 1:
                print('WARNING: multiple nifti files match {}: {}'.format(row['filename'], niftis), file=sys.stderr)
            scansAndFiles[scanId]['NIFTI'].extend(niftis)
            scansAndFiles[scanId]['BIDS'].append(bidsjson)
            print('{}: Found json {} and image {}'.format(scanId, bidsjson, niftis))

    for scanId in scansAndFiles.keys():
        for res in ['NIFTI', 'BIDS']:
            xnatSession.renew_httpsession()
            uri = '/data/experiments/%s/scans/%s/resources/%s' % (sessionId, scanId, res)
            print('Deleting {}'.format(uri))
            r = xnatSession.httpsess.delete(host + uri, params={'removeFiles':True})
            r.raise_for_status()
            tempdir = tempfile.mkdtemp()
            tempfilepath = os.path.join(tempdir, '%s%s%s.zip' % (sessionId, scanId, res))
            with zipfile.ZipFile(tempfilepath, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
                for f in scansAndFiles[scanId][res]:
                    print('Adding {}'.format(f))
                    zipf.write(f, os.path.basename(f))
            print('Uploading to {}'.format(uri))
            r = xnatSession.httpsess.put(host + uri + '/files', params=resMap[res], files={'file': open(tempfilepath, 'rb')})
            os.remove(tempfilepath)
            r.raise_for_status()

    #copy session-level files into outputDir
    print('Copying session-level BIDS files to {}'.format(outputDir))
    for f in os.listdir(sesDir):
        ff = os.path.join(sesDir, f)
        if os.path.isfile(ff):
            print("Copying {} to {}".format(ff, outputDir))
            shutil.copy(ff, outputDir)


version = '1.0'
args = docopt(__doc__, version=version)

inputDir = args['<inputDir>']
outputDir = args['<outputDir>']
print('Input dir: {}'.format(inputDir))
print('Output dir: {}'.format(outputDir))
host = os.environ['XNAT_HOST']
success = True

try:
    xnatSession = XnatSession(username=os.environ['XNAT_USER'], password=os.environ['XNAT_PASS'], host=host)

    scansTsvList = glob(os.path.join(inputDir, '**', '*_scans.tsv'), recursive=True)
    if len(scansTsvList) == 0:
        print('No scans.tsv files found', file=sys.stderr)
        sys.exit(1)

    for tsv in scansTsvList:
        try:
            print('Processing {}'.format(tsv))
            parseAndUpload(tsv)
        except Exception:
            traceback.print_exc()
            success = False
finally:
    xnatSession.close_httpsession()

if not success:
    sys.exit(1)
