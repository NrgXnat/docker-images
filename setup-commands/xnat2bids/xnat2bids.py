#!/usr/bin/env python

"""xnat2bids
Turn files in XNAT archive format into BIDS format.

Usage:
    xnat2bids.py <inputDir> <outputDir>
    xnat2bids.py (-h | --help)
    xnat2bids.py --version

Options:
    -h --help           Show the usage
    --version           Show the version
    <inputDir>          Directory with XNAT-archive-formatted files.
                        There should be scan directories, each having a NIFTI resource with NIFTI files, and
                        BIDS resources with BIDS sidecar JSON files.
    <outputDir>         Directory in which BIDS formatted files should be written.
"""

import os
import sys
import json
import shutil
import pathlib
import csv
import traceback
from glob import glob
from docopt import docopt
import xnatbidsfns

class BidsScan(object):
    def __init__(self, scanId, bidsNameMap, *args):
        self.scanId = scanId
        self.bidsNameMap = bidsNameMap
        self.subject = bidsNameMap.get('sub')
        self.session = bidsNameMap.get('ses')
        self.modality = bidsNameMap.get('modality')
        modalityLowercase = self.modality.lower()
        self.subDir = xnatbidsfns.getSubdir(self.modality)
        self.sourceFiles = list(args)

class BidsSession(object):
    def __init__(self, sessionLabel, inputDir, bidsScans=[]):
        self.sessionLabel = sessionLabel
        self.bidsScans = bidsScans
        self.inputDir = inputDir

class BidsSubject(object):
    def __init__(self, subjectLabel, bidsSession=None, bidsScans=[]):
        self.subjectLabel = subjectLabel
        if bidsSession:
            self.bidsSessions = [bidsSession]
            self.bidsScans = None
        if bidsScans:
            self.bidsScans = bidsScans
            self.bidsSessions = None

    def addBidsSession(self, bidsSession):
        if self.bidsScans:
            raise ValueError("Cannot add a BidsSession when the subject already has a list of BidsScans.")
        if not self.bidsSessions:
            self.bidsSessions = []
        self.bidsSessions.append(bidsSession)

    def hasSessions(self):
        return bool(self.bidsSessions is not None and self.bidsSessions is not [])

    def hasScans(self):
        return bool(self.bidsScans is not None and self.bidsScans is not [])


def bidsifySession(sessionDir, multiple = False):
    print("Checking for session structure in " + sessionDir)

    scansDir = os.path.join(sessionDir, 'SCANS')
    if not os.path.exists(scansDir):
        # I guess we don't have any scans with BIDS data in this session
        print("STOPPING. Could not find SCANS directory.")
        return

    print("Found SCANS directory. Checking scans for BIDS data.")

    bidsScans = []
    for scanId in os.listdir(scansDir):
        print("")
        print("Checking scan {}.".format(scanId))

        scanDir = os.path.join(scansDir, scanId)
        scanBidsDir = os.path.join(scanDir, 'BIDS')
        scanNiftiDir = os.path.join(scanDir, 'NIFTI')

        if not os.path.exists(scanBidsDir):
            # This scan does not have BIDS data
            print("SKIPPING. Scan {} does not have a BIDS directory.".format(scanId))
            continue

        scanBidsJsonGlobList = glob(scanBidsDir + '/*.json')
        if len(scanBidsJsonGlobList) == 0:
            print("SKIPPING. Scan {} does not have a BIDS json file.")
            continue
        elif len(scanBidsJsonGlobList) > 1:
            # Something went wrong here. We should only have one JSON file in this directory.
            print("WARNING. Scan {} has {} JSON files in its BIDS directory. I expected to see one and I'm using the first".format(scanId, len(scanBidsJsonGlobList)))
            for jsonFile in scanBidsJsonGlobList:
                print(jsonFile)
        scanBidsJsonFilePath = scanBidsJsonGlobList[0]
        scanBidsJsonFileName = os.path.basename(scanBidsJsonFilePath)
        scanBidsFileName = scanBidsJsonFileName.rstrip('.json')
        scanBidsNameMap = xnatbidsfns.generateBidsNameMap(scanBidsFileName)

        print("BIDS JSON file name: {}".format(scanBidsJsonFileName))
        print("Name map: {}".format(scanBidsNameMap))

        if not scanBidsNameMap.get('sub') or not scanBidsNameMap.get('modality'):
            # Either 'sub' or 'modality' or both weren't found. Something is wrong. Let's find out what.
            if not scanBidsNameMap.get('sub') and not scanBidsNameMap.get('modality'):
                print("SKIPPING. Neither 'sub' nor 'modality' could be parsed from the BIDS JSON file name.")
            elif not scanBidsNameMap.get('sub'):
                print("SKIPPING. Could not parse 'sub' from the BIDS JSON file name.")
            else:
                print("SKIPPING. Could not parse 'modality' from the BIDS JSON file name.")
            continue

        scanBidsDirFilePaths = glob(os.path.join(scanBidsDir, scanBidsFileName) + '.*')
        scanNiftiDirFilePaths = glob(os.path.join(scanNiftiDir, scanBidsFileName) + '.*')
        allFilePaths = scanBidsDirFilePaths + scanNiftiDirFilePaths

        bidsScan = BidsScan(scanId, scanBidsNameMap, *allFilePaths)
        if not bidsScan.subDir:
            print("SKIPPING. Could not determine subdirectory for modality {}.".format(bidsScan.modality))
            continue

        bidsScans.append(bidsScan)
        print("Done checking scan {}.".format(scanId))

    print("")
    print("Done checking all scans.")

    if bidsScans and not multiple:
        sessionBidsJsonPath = os.path.join(sessionDir, 'RESOURCES', 'BIDS', 'dataset_description.json')
        copyDatasetDescription(sessionBidsJsonPath)

    return bidsScans

def copyDatasetDescription(json):
    if not os.path.isfile(json):
        # Use a dummy file
        json = os.path.join(os.path.normpath('/root'), 'dataset_description.json')
    # Copy over the dataset_description as BIDS requires this
    print("Copying {} to {}".format(json, outputDir))
    shutil.copy(json, outputDir)

def getSubjectForBidsScans(bidsScanList):
    print("")
    print("Finding subject for list of BIDS scans.")
    subjects = list({bidsScan.subject for bidsScan in bidsScanList if bidsScan.subject})

    if len(subjects) == 1:
        print("Found subject {}.".format(subjects[0]))
        return subjects[0]
    elif len(subjects) > 1:
        print("ERROR: Found more than one subject: {}.".format(", ".join(subjects)))
    else:
        print("ERROR: Found no subjects.")

    return None

def getSessionForBidsScans(bidsScanList):
    print("")
    print("Finding session for list of BIDS scans.")
    sessions = list({bidsScan.session for bidsScan in bidsScanList if bidsScan.session})

    if len(sessions) == 1:
        print("Found session {}.".format(sessions[0]))
        return sessions[0]
    elif len(sessions) > 1:
        print("ERROR: Found more than one sessions: {}.".format(", ".join(sessions)))
    else:
        print("ERROR: Found no sessions.")

    return None

def relativePath(f):
    p = pathlib.Path(f)
    o = pathlib.Path(outputDir)
    return str(p.relative_to(o))

def copyScanBidsFiles(destDirBase, bidsScanList):
    # First make all the "anat", "func", etc. subdirectories that we will need
    for subDir in {scan.subDir for scan in bidsScanList}:
        os.mkdir(os.path.join(destDirBase, subDir))

    # Now go through all the scans and copy their files into the correct subdirectory
    for scan in bidsScanList:
        destDir = os.path.join(destDirBase, scan.subDir)
        for f in scan.sourceFiles:
            shutil.copy(f, destDir)

def manualBidsReorganization():
    # First check if the input directory is a session directory
    sessionBidsScans = bidsifySession(inputDir)
    
    bidsSubjectMap = {}
    if sessionBidsScans:
        subject = getSubjectForBidsScans(sessionBidsScans)
        if not subject:
            # We would have already printed an error message, so no need to print anything here
            sys.exit(1)
        session = getSessionForBidsScans(sessionBidsScans)
        if not session:
            bidsSubjectMap = {subject: BidsSubject(subject, bidsScans=sessionBidsScans)}
        else:
            bidsSession = BidsSession(session, inputDir, sessionBidsScans)
            bidsSubjectMap = {subject: BidsSubject(subject, bidsSession=bidsSession)}
    else:
        # Ok, we didn't find any BIDS scan directories in inputDir. We may be looking at a collection of session directories.
        copyDatasetDescription(os.path.join(inputDir, 'resources', 'BIDS', 'dataset_description.json'))
        print("")
        print("Checking subdirectories of {}.".format(inputDir))
    
        for subSessionDir in os.listdir(inputDir):
            inputDirSession = os.path.join(inputDir, subSessionDir)
            subSessionBidsScans = bidsifySession(inputDirSession, True)
            if subSessionBidsScans:
                subject = getSubjectForBidsScans(subSessionBidsScans)
                if not subject:
                    print("SKIPPING. Could not determine subject for session {}.".format(subSessionDir))
                    continue
    
                session = getSessionForBidsScans(subSessionBidsScans)
                print("Adding BIDS session {} to list for subject {}.".format(session, subject))
                bidsSession = BidsSession(session, inputDirSession, subSessionBidsScans)
                if subject not in bidsSubjectMap:
                    bidsSubjectMap[subject] = BidsSubject(subject, bidsSession=bidsSession)
                else:
                    bidsSubjectMap[subject].addBidsSession(bidsSession)
    
            else:
                print("No BIDS data found in session {}.".format(subSessionDir))
    
    print("")
    
    if not bidsSubjectMap:
        print("No BIDS data found anywhere in inputDir {}.".format(inputDir))
        sys.exit(1)
    
    print("")
    allHaveSessions = True
    allHaveScans = True
    for bidsSubject in bidsSubjectMap.values():
        allHaveSessions = allHaveSessions and bidsSubject.hasSessions()
        allHaveScans = allHaveScans and bidsSubject.hasScans()
    
    if not (allHaveSessions ^ allHaveScans):
        print("ERROR: Somehow we have a mix of subjects with explicit sessions and subjects without explicit sessions. We must have either all subjects with sessions, or all subjects without. They cannot be mixed.")
        sys.exit(1)
    
    print("Copying BIDS data.")
    for bidsSubject in bidsSubjectMap.values():
        subjectDir = os.path.join(outputDir, "sub-" + bidsSubject.subjectLabel)
        os.mkdir(subjectDir)
    
        if allHaveSessions:
            for bidsSession in bidsSubject.bidsSessions:
                sessionDir = os.path.join(subjectDir, "ses-" + bidsSession.sessionLabel)
                os.mkdir(sessionDir)
                copyScanBidsFiles(sessionDir, bidsSession.bidsScans)
        else:
            copyScanBidsFiles(subjectDir, bidsSubject.bidsScans)
    
    print("Done.")

def reorganizeWithTsv(tsvfile):
    print("Copying session-level BIDS files to output dir")
    copyDatasetDescription(os.path.join(os.path.dirname(tsvfile), 'dataset_description.json'))
    path = pathlib.Path(tsvfile)
    ii = path.parts.index('RESOURCES')
    sessionDir = os.path.join(*path.parts[:ii])
    print("Copying scan-level BIDS files to output dir per {}".format(tsvfile))
    sessionOutDir = None
    with open(tsvfile, 'r') as tsv:
        reader = csv.DictReader(tsv, delimiter='\t')
        for row in reader:
            # Copying scan-level BIDS files to output dir
            scanId = row['xnat_scan_id']
            scanSubdir, scanFname = pathlib.Path(row['filename']).parts
            if sessionOutDir is None:
                scanBidsNameMap = xnatbidsfns.generateBidsNameMap(scanFname)
                sessionOutDir = os.path.join(outputDir, "sub-" + scanBidsNameMap.get("sub"))
                if "ses" in scanBidsNameMap:
                    sessionOutDir = os.path.join(sessionOutDir, "ses-" + scanBidsNameMap.get("ses"))
                os.makedirs(sessionOutDir, exist_ok = True)
                print("Copying {} to {}".format(tsvfile, sessionOutDir))
                shutil.copy(tsvfile, sessionOutDir)
            scanOutDir = os.path.join(sessionOutDir, scanSubdir)
            os.makedirs(scanOutDir, exist_ok = True) 
            for f in glob(os.path.join(sessionDir, 'SCANS', scanId, 'NIFTI', scanFname + '.nii.*')) + \
                     glob(os.path.join(sessionDir, 'SCANS', scanId, 'BIDS', scanFname + '.json')):
                print("Copying {} to {}".format(f, scanOutDir))
                shutil.copy(f, scanOutDir)


version = "1.0"
args = docopt(__doc__, version=version)

inputDir = args['<inputDir>']
outputDir = args['<outputDir>']

print("Input dir: {}".format(inputDir))
print("Output dir: {}".format(outputDir))

# If we have scan.tsv file(s), use these, otherwise, perform manual reorganization
scansTsvList = glob(os.path.join(inputDir, '**', 'RESOURCES', 'BIDS', '*_scans.tsv'), recursive=True)
if len(scansTsvList) == 0:
    manualBidsReorganization()
else:
    success = True
    for tsv in scansTsvList:
        try:
            print('Reorganizing into BIDS structure per {}'.format(tsv))
            reorganizeWithTsv(tsv)
        except Exception:
            traceback.print_exc()
            success = False
   
