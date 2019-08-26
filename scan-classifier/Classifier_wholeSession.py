#!/usr/bin/python

import os, sys, errno, shutil, uuid
import math
import glob
import re
import requests
import pydicom as dicom

from xnatSession import XnatSession
import DecompressDCM
import label_probability

catalogXmlRegex = re.compile(r'.*\.xml$')

def get_dicom_for_scanid(sessionDir, scanId):
    print("Locating DICOM files for scan %s" % scanId)
    for dirn in ["SCANS", "RAW"]:
        scanDir = os.path.join(sessionDir, dirn, scanId)
        print("Checking %s" % scanDir)
        if not os.path.isdir(scanDir):
            continue
        for dcm in glob.iglob(os.path.join(scanDir, "**"), recursive=True):
            if os.path.isdir(dcm):
                continue
            try:
                # Test if it's a DICOM file, if so, gather all in series and return the slice 70% thru brain
                dicomDs = dicom.filereader.dcmread(dcm)
                dicomFiles = [fl for fl in glob.iglob(os.path.join(os.path.dirname(dcm), "*")) if not catalogXmlRegex.match(fl)]
                nDicomFiles = len(dicomFiles)
                t = min(nDicomFiles-1, math.ceil(nDicomFiles*0.7)) # slice 70% through the brain
                selDicom = dicomFiles[t]
                print("Found %s DICOM files, using %s for snapshot" % (nDicomFiles, selDicom))
                return (selDicom, nDicomFiles)
            except (dicom.errors.InvalidDicomError, IsADirectoryError):
                # Skip, not a dicom
                pass
    #TODO add handling for DICOM files that are not stored in a directory matching their XNAT scanId
    raise Exception("No DICOM files found for %s" % scanId)
    

def run_classifier(sessionDir, rawDir, jpgDir, sessionId, scanId, xnatSession):
    print("Classifying scan %s" % scanId)
    # Select DICOM file for scanId (70% thru the brain)
    (selDicom, nDicomFiles) = get_dicom_for_scanid(sessionDir, scanId)
    # Decompress it (just a copy if not compressed)
    selDicomDecompr = os.path.join(rawDir, os.path.basename(selDicom))
    DecompressDCM.decompress(selDicom, selDicomDecompr)
    # Classify it
    label = label_probability.classify(selDicomDecompr, jpgDir, scanId, nDicomFiles)
    print("Scan classification for %s scan %s is '%s'" % (sessionId, scanId, label))
    # Change value of series_class in XNAT
    url = ("/data/experiments/%s/scans/%s?xsiType=xnat:mrScanData&xnat:imageScanData/series_class=%s" % 
        (sessionId, scanId, label))
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.put(xnatSession.host + url)
    if response.status_code == 200 or response.status_code == 201:
        print("Successfully set series_class for %s scan %s to '%s'" % (sessionId, scanId, label))
    else:
        errStr = "ERROR"
        if response.status_code == 403 or response.status_code == 404:
            errStr = "PERMISSION DENIED"
        raise Exception("%s attempting to set series_class for %s %s to '%s': %s" % 
            (errStr, sessionId, scanId, label, response.text))


if __name__ == '__main__':
    # Get user args
    if len(sys.argv) != 5:
        sys.stderr.write("Usage: %s [session directory] [working directory] [XNAT session ID] [quoted space-delimited list of scan ids]" % sys.argv[0])
        exit(1)

    sessionDir = sys.argv[1]
    workingDir = sys.argv[2]
    sessionId = sys.argv[3]
    scans = sys.argv[4].split()

    # Make working dirs
    rawDir = os.path.join(workingDir, 'RAW')
    os.makedirs(rawDir)
    jpgDir = os.path.join(workingDir, 'JPG' )
    os.makedirs(jpgDir)

    # Prep XNAT session
    XNAT_HOST = os.environ['XNAT_HOST']
    XNAT_USER = os.environ['XNAT_USER']
    XNAT_PASS = os.environ['XNAT_PASS']
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)

    # Run classifier
    nFail = 0
    for scanId in scans:
        try:
            run_classifier(sessionDir, rawDir, jpgDir, sessionId, scanId, xnatSession)
        except Exception as e:
            nFail += 1
            sys.stderr.write("Error attempting to classify %s %s: %s\n" % (sessionId, scanId, str(e)))

    # Cleanup
    xnatSession.close_httpsession()
    shutil.rmtree(rawDir)
    shutil.rmtree(jpgDir)

    if nFail == len(scans):
        # Everything failed, return error
        exit(1)
