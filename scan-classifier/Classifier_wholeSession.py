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

def get_slice_idx(nDicomFiles):
    return min(nDicomFiles-1, math.ceil(nDicomFiles*0.7)) # slice 70% through the brain


def get_dicom_from_filesystem(sessionDir, scanId):
    print("Locating DICOM files for scan %s" % scanId)
    for dirn in ["SCANS", "RAW"]:
        scanDir = os.path.join(sessionDir, dirn, scanId)
        print("Checking %s" % scanDir)
        if not os.path.isdir(scanDir):
            continue
        for dcm in glob.iglob(os.path.join(scanDir, "**"), recursive=True):
            try:
                # Test if it's a DICOM file
                dicomDs = dicom.filereader.dcmread(dcm)
                # Gather all in series and return the slice 70% thru brain
                dicomFiles = [fl for fl in glob.iglob(os.path.join(os.path.dirname(dcm), "*")) if not catalogXmlRegex.match(fl)]
                nDicomFiles = len(dicomFiles)
                selDicom = dicomFiles[get_slice_idx(nDicomFiles)]
                print("Found %s DICOM files, using %s for snapshot" % (nDicomFiles, selDicom))
                return selDicom, nDicomFiles
            except (dicom.errors.InvalidDicomError, IsADirectoryError):
                # Skip, not a dicom
                pass
    raise Exception("No DICOM files found for %s" % scanId)


def get_dicom_from_xnat(sessionId, scanId, sessionDir, xnatSesDir, xnatSession):
    # Handle DICOM files that are not stored in a directory matching their XNAT scanId
    print("No DICOM found in %s directory, querying XNAT for DICOM path" % scanId)
    url = ("/data/experiments/%s/scans/%s/files?format=json&locator=absolutePath&file_format=DICOM" % 
        (sessionId, scanId))
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(xnatSession.host + url)
    if response.status_code != 200:
        raise Exception("Error querying XNAT for %s DICOM files: %s %s %s" % (scanId, 
                                                                              response.status_code, 
                                                                              response.reason, 
                                                                              response.text))
    result = response.json()['ResultSet']['Result']
    nDicomFiles = len(result)
    if nDicomFiles == 0:
        raise Exception("No DICOM files for %s stored in XNAT" % scanId)

    # Get 70% file and ensure it exists
    selDicomAbs = result[get_slice_idx(nDicomFiles)]['absolutePath']
    selDicom = os.path.join(sessionDir, os.path.relpath(selDicomAbs, xnatSesDir))
    if not os.path.isfile(selDicom):
        raise Exception("Cannot locate %s as %s on filesystem" % (selDicomAbs, selDicom))

    print("Found %s DICOM files, using %s for snapshot" % (nDicomFiles, selDicom))
    return selDicom, nDicomFiles


def run_classifier(sessionDir, rawDir, jpgDir, sessionId, scanId, xnatSesDir, xnatSession):
    print("Classifying scan %s" % scanId)
    # Select DICOM file for scanId (70% thru the brain)
    try:
        # Try looking through the filesystem first to avoid a ton of API calls to XNAT
        selDicom, nDicomFiles = get_dicom_from_filesystem(sessionDir, scanId)
    except Exception:
        # But fall back on the API if needed
        selDicom, nDicomFiles = get_dicom_from_xnat(sessionId, scanId, sessionDir, xnatSesDir, xnatSession)
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
    if len(sys.argv) != 6:
        sys.stderr.write("Usage: %s [session directory] [working directory] [XNAT session ID] \
            [XNAT session directory] [quoted space-delimited list of scan ids]" % sys.argv[0])
        exit(1)

    sessionDir = sys.argv[1]
    workingDir = sys.argv[2]
    sessionId = sys.argv[3]
    xnatSesDir = sys.argv[4]
    scans = sys.argv[5].split()

    # Make working dirs
    rawDir = os.path.join(workingDir, 'RAW')
    os.makedirs(rawDir, exist_ok = True)
    jpgDir = os.path.join(workingDir, 'JPG' )
    os.makedirs(jpgDir, exist_ok = True)

    # Prep XNAT session
    XNAT_HOST = os.environ['XNAT_HOST']
    XNAT_USER = os.environ['XNAT_USER']
    XNAT_PASS = os.environ['XNAT_PASS']
    xnatSession = XnatSession(username=XNAT_USER, password=XNAT_PASS, host=XNAT_HOST)

    # Run classifier
    nFail = 0
    for scanId in scans:
        try:
            run_classifier(sessionDir, rawDir, jpgDir, sessionId, scanId, xnatSesDir, xnatSession)
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
