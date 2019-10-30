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
from glob import glob
from docopt import docopt

bidsAnatModalities = ['t1w', 't2w', 't1rho', 't1map', 't2map', 't2star', 'flair', 'flash', 'pd', 'pdmap', 'pdt2', 'inplanet1', 'inplanet2', 'angio', 'defacemask', 'swimagandphase']
bidsFuncModalities = ['bold', 'physio', 'stim', 'sbref']
bidsDwiModalities = ['dwi', 'dti']
bidsBehavioralModalities = ['beh']
bidsFieldmapModalities = ['phasemap', 'magnitude1']

class BidsScan(object):
    def __init__(self, scanId, bidsNameMap, *args):
        self.scanId = scanId
        self.bidsNameMap = bidsNameMap
        self.subject = bidsNameMap.get('sub')
        self.modality = bidsNameMap.get('modality')
        modalityLowercase = self.modality.lower()
        self.subDir = 'anat' if modalityLowercase in bidsAnatModalities else \
                      'func' if modalityLowercase in bidsFuncModalities else \
                      'dwi' if modalityLowercase in bidsDwiModalities else \
                      'beh' if modalityLowercase in bidsBehavioralModalities else \
                      'fmap' if modalityLowercase in bidsFieldmapModalities else \
                      None
        self.sourceFiles = list(args)

class BidsSession(object):
    def __init__(self, sessionLabel, bidsScans=[]):
        self.sessionLabel = sessionLabel
        self.bidsScans = bidsScans

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

def generateBidsNameMap(bidsFileName):

    # The BIDS file names will look like
    # sub-<participant_label>[_ses-<session_label>][_acq-<label>][_ce-<label>][_rec-<label>][_run-<index>][_mod-<label>]_<modality_label>
    # (that example is for anat. There may be other fields and labels in the other file types.)
    # So we split by underscores to get the individual field values.
    # However, some of the values may contain underscores themselves, so we have to check that each entry (save the last)
    #   contains a -.
    underscoreSplitListRaw = bidsFileName.split('_')
    underscoreSplitList = []

    for splitListEntryRaw in underscoreSplitListRaw[:-1]:
        if '-' not in splitListEntryRaw:
            underscoreSplitList[-1] = underscoreSplitList[-1] + splitListEntryRaw
        else:
            underscoreSplitList.append(splitListEntryRaw)

    bidsNameMap = dict(splitListEntry.split('-') for splitListEntry in underscoreSplitList)
    bidsNameMap['modality'] = underscoreSplitListRaw[-1]

    return bidsNameMap

def bidsifySession(sessionDir):
    print("Checking for session structure in " + sessionDir)

    sessionBidsJsonPath = os.path.join(sessionDir, 'RESOURCES', 'BIDS', 'dataset_description.json')
    # Copy over the dataset_description as BIDS requires this
    shutil.copy2(sessionBidsJsonPath, outputDir)

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
        if len(scanBidsJsonGlobList) != 1:
            # Something went wrong here. We should only have one JSON file in this directory.
            print("SKIPPING. Scan {} has {} JSON files in its BIDS directory. I expected to see one.".format(scanId, len(scanBidsJsonGlobList)))
            for jsonFile in scanBidsJsonGlobList:
                print(jsonFile)
            continue
        scanBidsJsonFilePath = scanBidsJsonGlobList[0]
        scanBidsJsonFileName = os.path.basename(scanBidsJsonFilePath)
        scanBidsFileName = scanBidsJsonFileName.rstrip('.json')
        scanBidsNameMap = generateBidsNameMap(scanBidsFileName)

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
    return bidsScans

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

def copyScanBidsFiles(destDirBase, bidsScanList):
    # First make all the "anat", "func", etc. subdirectories that we will need
    for subDir in {scan.subDir for scan in bidsScanList}:
        os.mkdir(os.path.join(destDirBase, subDir))

    # Now go through all the scans and copy their files into the correct subdirectory
    for scan in bidsScanList:
        destDir = os.path.join(destDirBase, scan.subDir)
        for f in scan.sourceFiles:
            shutil.copy(f, destDir)

version = "1.0"
args = docopt(__doc__, version=version)

inputDir = args['<inputDir>']
outputDir = args['<outputDir>']

print("Input dir: {}".format(inputDir))
print("Output dir: {}".format(outputDir))

# First check if the input directory is a session directory
sessionBidsScans = bidsifySession(inputDir)

bidsSubjectMap = {}
if sessionBidsScans:
    subject = getSubjectForBidsScans(sessionBidsScans)
    if not subject:
        # We would have already printed an error message, so no need to print anything here
        sys.exit(1)
    bidsSubjectMap = {subject: BidsSubject(subject, bidsScans=sessionBidsScans)}
else:
    # Ok, we didn't find any BIDS scan directories in inputDir. We may be looking at a collection of session directories.
    print("")
    print("Checking subdirectories of {}.".format(inputDir))

    for subSessionDir in os.listdir(inputDir):
        subSessionBidsScans = bidsifySession(os.path.join(inputDir, subSessionDir))
        if subSessionBidsScans:
            subject = getSubjectForBidsScans(subSessionBidsScans)
            if not subject:
                print("SKIPPING. Could not determine subject for session {}.".format(subSessionDir))
                continue

            print("Adding BIDS session {} to list for subject {}.".format(subSessionDir, subject))
            bidsSession = BidsSession(subSessionDir, subSessionBidsScans)
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
for bidsSubject in bidsSubjectMap.itervalues():
    allHaveSessions = allHaveSessions and bidsSubject.hasSessions()
    allHaveScans = allHaveScans and bidsSubject.hasScans()

if not (allHaveSessions ^ allHaveScans):
    print("ERROR: Somehow we have a mix of subjects with explicit sessions and subjects without explicit sessions. We must have either all subjects with sessions, or all subjects without. They cannot be mixed.")
    sys.exit(1)

print("Copying BIDS data.")
for bidsSubject in bidsSubjectMap.itervalues():
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
