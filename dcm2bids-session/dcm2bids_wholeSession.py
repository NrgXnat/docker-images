import argparse
import collections
import json
import requests
import os
import glob
import sys
import subprocess
import time
import zipfile
import tempfile
import re
import csv
import dicom as dicomLib
from shutil import copy as fileCopy
from nipype.interfaces.dcm2nii import Dcm2nii
from collections import OrderedDict
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

from xnatjsession import XnatSession
import xnatbidsfns

def cleanServer(server):
    server.strip()
    if server[-1] == '/':
        server = server[:-1]
    if server.find('http') == -1:
        server = 'https://' + server
    return server


def isTrue(arg):
    return arg is not None and (arg == 'Y' or arg == '1' or arg == 'True')


def download(name, pathDict):
    if not os.access(pathDict['absolutePath'], os.R_OK):
        raise IOError("Unable to read %s" % pathDict['absolutePath'])
    #if os.access(pathDict['absolutePath'], os.R_OK):
    #    try:
    #        os.symlink(pathDict['absolutePath'], name)
    #    except:
    #        fileCopy(pathDict['absolutePath'], name)
    #        print 'Copied %s.' % pathDict['absolutePath']
    #else:
    #    with open(name, 'wb') as f:
    #        r = get(pathDict['URI'], stream=True)
    #
    #        for block in r.iter_content(1024):
    #            if not block:
    #                break
    #
    #            f.write(block)
    #    print 'Downloaded file %s.' % name

def zipdir(dirPath=None, zipFilePath=None, includeDirInZip=True):
    if not zipFilePath:
        zipFilePath = dirPath + ".zip"
    if not os.path.isdir(dirPath):
        raise OSError("dirPath argument must point to a directory. "
            "'%s' does not." % dirPath)
    parentDir, dirToZip = os.path.split(dirPath)
    def trimPath(path):
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not includeDirInZip:
            archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
        return os.path.normcase(archivePath)
    with zipfile.ZipFile(zipFilePath, "w", compression=zipfile.ZIP_DEFLATED) as outFile:
        for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
            for fileName in fileNames:
                filePath = os.path.join(archiveDirPath, fileName)
                outFile.write(filePath, trimPath(filePath))
            # Make sure we get empty directories as well
            if not fileNames and not dirNames:
                zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
                # some web sites suggest doing
                # zipInfo.external_attr = 16
                # or
                # zipInfo.external_attr = 48
                # Here to allow for inserting an empty directory.  Still TBD/TODO.
                outFile.writestr(zipInfo, "")


BIDSVERSION = "1.0.1"

parser = argparse.ArgumentParser(description="Run dcm2niix on every file in a session")
parser.add_argument("--host", default="https://cnda.wustl.edu", help="CNDA host", required=True)
parser.add_argument("--user", help="CNDA username", required=True)
parser.add_argument("--password", help="Password", required=True)
parser.add_argument("--session", help="Session ID", required=True)
parser.add_argument("--sessionLabel", help="Session Label", required=True)
parser.add_argument("--subject", help="Subject Label", required=False)
parser.add_argument("--project", help="Project", required=False)
parser.add_argument("--dicomdir", help="Root output directory for DICOM files", required=True)
parser.add_argument("--niftidir", help="Root output directory for NIFTI files", required=True)
parser.add_argument("--overwrite", help="Overwrite NIFTI files if they exist")
parser.add_argument("--upload-by-ref", help="Upload \"by reference\". Only use if your host can read your file system.")
parser.add_argument("--workflowId", help="Pipeline workflow ID")
parser.add_argument("--skipUnusable", help="Skip scans with quality=unusable")
parser.add_argument('--version', action='version', version='%(prog)s 1')

args, unknown_args = parser.parse_known_args()
host = cleanServer(args.host)
session = args.session
sessionLabel = args.sessionLabel
subject = args.subject
project = args.project
overwrite = isTrue(args.overwrite)
dicomdir = args.dicomdir
niftidir = args.niftidir
workflowId = args.workflowId
uploadByRef = isTrue(args.upload_by_ref)
skipUnusable = isTrue(args.skipUnusable)
dcm2niixArgs = unknown_args if unknown_args is not None else []

imgdir = niftidir + "/IMG"
bidsdir = niftidir + "/BIDS"

builddir = os.getcwd()

# Set up working directory
if not os.access(dicomdir, os.R_OK):
    print 'Making DICOM directory %s' % dicomdir
    os.mkdir(dicomdir)
if not os.access(niftidir, os.R_OK):
    print 'Making NIFTI directory %s' % niftidir
    os.mkdir(niftidir)
if not os.access(imgdir, os.R_OK):
    print 'Making NIFTI image directory %s' % imgdir
    os.mkdir(imgdir)
if not os.access(bidsdir, os.R_OK):
    print 'Making NIFTI BIDS directory %s' % bidsdir
    os.mkdir(bidsdir)

try:
    # Set up session
    xnatSession = XnatSession(username=args.user, password=args.password, host=host)
    
    def get(url, **kwargs):
        try:
            xnatSession.renew_httpsession()
            r = xnatSession.httpsess.get(url, **kwargs)
            r.raise_for_status()
        except (requests.ConnectionError, requests.exceptions.RequestException) as e:
            print "Request Failed"
            print "    " + str(e)
            sys.exit(1)
        return r
    
    if project is None or subject is None:
        # Get project ID and subject ID from session JSON
        print "Get project and subject ID for session ID %s." % session
        r = get(host + "/data/experiments/%s" % session, params={"format": "json", "handler": "values", "columns": "project,subject_ID"})
        sessionValuesJson = r.json()["ResultSet"]["Result"][0]
        project = sessionValuesJson["project"] if project is None else project
        subjectID = sessionValuesJson["subject_ID"]
        print "Project: " + project
        print "Subject ID: " + subjectID
    
        if subject is None:
            print
            print "Get subject label for subject ID %s." % subjectID
            r = get(host + "/data/subjects/%s" % subjectID, params={"format": "json", "handler": "values", "columns": "label"})
            subject = r.json()["ResultSet"]["Result"][0]["label"]
            print "Subject label: " + subject
    
    # Get list of scan ids
    print
    print "Get scan list for session ID %s." % session
    r = get(host + "/data/experiments/%s/scans" % session, params={"format": "json", "columns": "ID,quality,series_description,type"})
    scanRequestResultList = r.json()["ResultSet"]["Result"]
    if skipUnusable:
        scanIDList = []
        seriesDescList = []
        typeList = []
        for scan in scanRequestResultList:
            if scan['quality'] == "unusable":
                print "Skiping %s because its quality=unusable" % scan['ID']
                continue
            scanIDList.append(scan['ID'])
            seriesDescList.append(scan['series_description'])
            typeList.append(scan['type'])
    else: 
        scanIDList = [scan['ID'] for scan in scanRequestResultList]
        seriesDescList = [scan['series_description'] for scan in scanRequestResultList]  # { id: sd for (scan['ID'], scan['series_description']) in scanRequestResultList }
        typeList = [scan['type'] for scan in scanRequestResultList]

    print 'Found scans %s.' % ', '.join(scanIDList)
    print 'Series descriptions %s' % ', '.join(seriesDescList)
    
    # Fall back on scan type if series description field is empty
    if set(seriesDescList) == set(['']):
        seriesDescList = typeList
        print 'Fell back to scan types %s' % ', '.join(seriesDescList)
    
    # Get site- and project-level configs
    bidsmaplist = []
    print
    print "Get site-wide BIDS map"
    # We don't use the convenience get() method because that throws exceptions when the object is not found.
    r = xnatSession.httpsess.get(host + "/data/config/bids/bidsmap", params={"contents": True})
    if r.ok:
        bidsmaptoadd = r.json()
        for mapentry in bidsmaptoadd:
            if mapentry not in bidsmaplist:
                bidsmaplist.append(mapentry)
    else:
        print "Could not read site-wide BIDS map"
    
    print "Get project BIDS map if one exists"
    r = xnatSession.httpsess.get(host + "/data/projects/%s/config/bids/bidsmap" % project, params={"contents": True})
    if r.ok:
        bidsmaptoadd = r.json()
        for mapentry in bidsmaptoadd:
            if mapentry not in bidsmaplist:
                bidsmaplist.append(mapentry)
    else:
        print "Could not read project BIDS map"
    
    # print "BIDS map: " + json.dumps(bidsmaplist)
    
    # Collapse human-readable JSON to dict for processing
    bidsnamemap = {x['series_description'].lower(): x['bidsname'] for x in bidsmaplist if 'series_description' in x and 'bidsname' in x}
    
    # Map all series descriptions to BIDS names (case insensitive)
    resolved = [bidsnamemap[x.lower()] for x in seriesDescList if x.lower() in bidsnamemap]
    
    # Count occurrences
    bidscount = collections.Counter(resolved)
    
    # Remove multiples
    multiples = {seriesdesc: count for seriesdesc, count in bidscount.viewitems() if count > 1}
    
    # BIDS base name (BIDS reserves _ and - so remove these)
    base = "sub-" + re.sub(r"[_-]", "", subject) + "_ses-" + re.sub(r"[_-]", "", sessionLabel) + "_"
    print "Bids base name is %s" % base
    
    # Cheat and reverse scanid and seriesdesc lists so numbering is in the right order
    scansTsv = []
    for scanid, seriesdesc in zip(reversed(scanIDList), reversed(seriesDescList)):
        print
        print 'Beginning process for scan %s.' % scanid
        os.chdir(builddir)
    
        print 'Assigning BIDS name for scan %s.' % scanid
    
        if seriesdesc.lower() not in bidsnamemap:
            print "Series " + seriesdesc + " not found in BIDSMAP"
            # bidsname = "Z"
            continue  # Exclude series from processing
        else:
            print "Series " + seriesdesc + " matched " + bidsnamemap[seriesdesc.lower()]
            match = bidsnamemap[seriesdesc.lower()]
    
        # split before last _
        splitname = match.split("_")
    
        # Check for multiples
        if match in multiples:
            # insert run-0x
            run = 'run-%02d' % multiples[match]
            splitname.insert(len(splitname) - 1, run)
    
            # decrement count
            multiples[match] -= 1
    
            # rejoin as string
            bidsname = "_".join(splitname)
        else:
            bidsname = match

        bidsname = base + bidsname
        print "Base " + base + " series " + seriesdesc + " match " + bidsname
        bidssubdir = xnatbidsfns.getSubdir(xnatbidsfns.generateBidsNameMap(bidsname)['modality'])
        if bidssubdir is None:
            print "Scan %s is assigned bidsname %s, which does NOT map to a bids subdirectory. Skipping" % (scanid, bidsname)
            continue
        bidsfilename = os.path.join(bidssubdir, bidsname)
    
        # Get scan resources
        print "Get scan resources for scan %s." % scanid
        r = get(host + "/data/experiments/%s/scans/%s/resources" % (session, scanid), params={"format": "json"})
        scanResources = r.json()["ResultSet"]["Result"]
        print 'Found resources %s.' % ', '.join(res["label"] for res in scanResources)
    
        ##########
        # Do initial checks to determine if scan should be skipped
        hasNifti = any([res["label"] == "NIFTI" for res in scanResources])  # Store this for later
        if hasNifti and not overwrite:
            # Add entry to scans.tsv
            scansTsv.append([bidsfilename, session, scanid])
            print "Scan %s has a preexisting NIFTI resource, and I am running with overwrite=False. Skipping." % scanid
            continue
    
        dicomResourceList = [res for res in scanResources if res["label"] == "DICOM"]
        imaResourceList = [res for res in scanResources if res["format"] == "IMA"]
    
        if len(dicomResourceList) == 0 and len(imaResourceList) == 0:
            print "Scan %s has no DICOM or IMA resource." % scanid
            # scanInfo['hasDicom'] = False
            continue
        elif len(dicomResourceList) == 0 and len(imaResourceList) > 1:
            print "Scan %s has more than one IMA resource and no DICOM resource. Skipping." % scanid
            # scanInfo['hasDicom'] = False
            continue
        elif len(dicomResourceList) > 1 and len(imaResourceList) == 0:
            print "Scan %s has more than one DICOM resource and no IMA resource. Skipping." % scanid
            # scanInfo['hasDicom'] = False
            continue
        elif len(dicomResourceList) > 1 and len(imaResourceList) > 1:
            print "Scan %s has more than one DICOM resource and more than one IMA resource. Skipping." % scanid
            # scanInfo['hasDicom'] = False
            continue
    
        dicomResource = dicomResourceList[0] if len(dicomResourceList) > 0 else None
        imaResource = imaResourceList[0] if len(imaResourceList) > 0 else None
    
        usingDicom = True if (len(dicomResourceList) == 1) else False
    
        if dicomResource is not None and dicomResource["file_count"]:
            if int(dicomResource["file_count"]) == 0:
                print "DICOM resource for scan %s has no files. Checking IMA resource." % scanid
                if imaResource["file_count"]:
                    if int(imaResource["file_count"]) == 0:
                        print "IMA resource for scan %s has no files either. Skipping." % scanid
                        continue
                else:
                    print "IMA resource for scan %s has a blank \"file_count\", so I cannot check it to see if there are no files. I am not skipping the scan, but this may lead to errors later if there are no files." % scanid
        elif imaResource is not None and imaResource["file_count"]:
            if int(imaResource["file_count"]) == 0:
                print "IMA resource for scan %s has no files. Skipping." % scanid
                continue
        else:
            print "DICOM and IMA resources for scan %s both have a blank \"file_count\", so I cannot check to see if there are no files. I am not skipping the scan, but this may lead to errors later if there are no files." % scanid
    
        ###########
        ## Prepare DICOM directory structure
        #print
        #scanDicomDir = os.path.join(dicomdir, scanid)
        #if not os.path.isdir(scanDicomDir):
        #    print 'Making scan DICOM directory %s.' % scanDicomDir
        #    os.mkdir(scanDicomDir)
        ## Remove any existing files in the builddir.
        ## This is unlikely to happen in any environment other than testing.
        #for f in os.listdir(scanDicomDir):
        #    os.remove(os.path.join(scanDicomDir, f))
    
        ##########
        # Get list of DICOMs/IMAs
    
        # set resourceid. This will only be set if hasIma is true and we've found a resource id
        resourceid = None
    
        if not usingDicom:
    
            print 'Get IMA resource id for scan %s.' % scanid
            r = get(host + "/data/experiments/%s/scans/%s/resources" % (session, scanid), params={"format": "json"})
            resourceDict = {resource['format']: resource['xnat_abstractresource_id'] for resource in r.json()["ResultSet"]["Result"]}
    
            if resourceDict["IMA"]:
                resourceid = resourceDict["IMA"]
            else:
                print "Couldn't get xnat_abstractresource_id for IMA file list."
    
        # Deal with DICOMs
        print 'Get list of DICOM files for scan %s.' % scanid
    
        if usingDicom:
            filesURL = host + "/data/experiments/%s/scans/%s/resources/DICOM/files" % (session, scanid)
        elif resourceid is not None:
            filesURL = host + "/data/experiments/%s/scans/%s/resources/%s/files" % (session, scanid, resourceid)
        else:
            print "Trying to convert IMA files but there is no resource id available. Skipping."
            continue
    
        r = get(filesURL, params={"format": "json", "locator": "absolutePath"})
        # I don't like the results being in a list, so I will build a dict keyed off file name
        dicomFileDict = {dicom['Name']: {'absolutePath': dicom['absolutePath']} for dicom in r.json()["ResultSet"]["Result"]}
    
        ##########
        # Download DICOMs
        print "Checking files for scan %s." % scanid
    
        # Check secondary
        # Download any one DICOM from the series and check its headers
        # If the headers indicate it is a secondary capture, we will skip this series.
        dicomFileList = dicomFileDict.items()
    
        (name, pathDict) = dicomFileList[0]
        scanDicomDir = os.path.dirname(pathDict['absolutePath'])
        os.chdir(scanDicomDir)
        try:
            download(name, pathDict)
        except Exception as e:
            sys.stderr.write(str(e))
            continue
    
        if usingDicom:
            print 'Checking modality in DICOM headers of file %s.' % name
            d = dicomLib.read_file(name)
            modalityHeader = d.get((0x0008, 0x0060), None)
            if modalityHeader:
                print 'Modality header: %s' % modalityHeader
                modality = modalityHeader.value.strip("'").strip('"')
                if modality == 'SC' or modality == 'SR':
                    print 'Scan %s is a secondary capture. Skipping.' % scanid
                    continue
            else:
                print 'Could not read modality from DICOM headers. Skipping.'
                continue
    
        ##########
        # Download remaining DICOMs
        for name, pathDict in dicomFileList[1:]:
            try:
                download(name, pathDict)
            except Exception as e:
                sys.stderr.write(str(e))
                continue
    
        os.chdir(builddir)
        print 'Done downloading for scan %s.' % scanid
        print
    
        ##########
        # Prepare NIFTI directory structure
        scanBidsDir = os.path.join(bidsdir, scanid)
        if not os.path.isdir(scanBidsDir):
            print 'Creating scan NIFTI BIDS directory %s.' % scanBidsDir
            os.mkdir(scanBidsDir)
    
        scanImgDir = os.path.join(imgdir, scanid)
        if not os.path.isdir(scanImgDir):
            print 'Creating scan NIFTI image directory %s.' % scanImgDir
            os.mkdir(scanImgDir)
    
        # Remove any existing files in the builddir.
        # This is unlikely to happen in any environment other than testing.
        for f in os.listdir(scanBidsDir):
            os.remove(os.path.join(scanBidsDir, f))
    
        for f in os.listdir(scanImgDir):
            os.remove(os.path.join(scanImgDir, f))
    
        # Convert the differences
        print 'Converting scan %s to NIFTI...' % scanid
        # Do some stuff to execute dcm2niix as a subprocess
    
        if usingDicom:
            dcm2niix_command = "dcm2niix -b y -z y".split() + dcm2niixArgs + " -f {} -o {} {}".format(bidsname, scanBidsDir, scanDicomDir).split()
            print "Executing command: " + " ".join(dcm2niix_command)
            print subprocess.check_output(dcm2niix_command)
        else:
            # call dcm2nii for converting ima files
            print subprocess.check_output("dcm2nii -b @PIPELINE_DIR_PATH@/catalog/DicomToBIDS/resources/dcm2nii.ini -g y -f Y -e N -p N -d N -o {} {}".format(scanBidsDir, scanDicomDir).split())
    
            #print subprocess.check_output("mv {}/*.nii.gz {}/{}.nii.gz".format(scanBidsDir, scanBidsDir, "bidsname").split())
    
            # there should only be one file in this folder
            for files in glob.glob(os.path.join(scanBidsDir, "*.nii.gz")):
                os.rename(files, os.path.join(scanBidsDir, bidsname + ".nii.gz"))
    
            # Create BIDS sidecar file from IMA XML
            imaSessionURL = host + "/data/archive/experiments/%s/scans/%s" % (session, scanid)
            r = get(imaSessionURL, params={"format": "json"})
    
            # fields from ima json result
            imaResultChildren = r.json()["items"][0]["children"][1]["items"][0]["data_fields"]
            imaResultDataFields = r.json()["items"][0]["data_fields"]
    
            #fileDimX = imaResultChildren["dimensions/x"] if "dimensions/x" in imaResultChildren else None
            #fileDimY = imaResultChildren["dimensions/y"] if "dimensions/y" in imaResultChildren else None
            #fileDimZ = imaResultChildren["dimensions/z"] if "dimensions/z" in imaResultChildren else None
            #fileDimVolumes = imaResultChildren["dimensions/volumes"] if "dimensions/volumes" in imaResultChildren else None
            #fileVoxelResX = imaResultChildren["voxelRes/x"] if "voxelRes/x" in imaResultChildren else None
            #fileVoxelResY = imaResultChildren["voxelRes/y"] if "voxelRes/y" in imaResultChildren else None
            #fileVoxelResZ = imaResultChildren["voxelRes/z"] if "voxelRes/z" in imaResultChildren else None
            #fileVoxelResUnits = imaResultChildren["voxelRes/units"] if "voxelRes/units" in imaResultChildren else None
            #fileOrientation = imaResultChildren["orientation"] if "orientation" in imaResultChildren else None
            #parametersFovX = imaResultDataFields["parameters/fov/x"] if "parameters/fov/x" in imaResultDataFields else None
            #parametersFovY = imaResultDataFields["parameters/fov/y"] if "parameters/fov/y" in imaResultDataFields else None
            #parametersMatrixX = imaResultDataFields["parameters/matrix/x"] if "parameters/matrix/x" in imaResultDataFields else None
            #parametersMatrixY = imaResultDataFields["parameters/matrix/y"] if "parameters/matrix/y" in imaResultDataFields else None
            parametersTr = imaResultDataFields["parameters/tr"] if "parameters/tr" in imaResultDataFields else None
            parametersTe = imaResultDataFields["parameters/te"] if "parameters/te" in imaResultDataFields else None
            parametersFlip = imaResultDataFields["parameters/flip"] if "parameters/flip" in imaResultDataFields else None
            #parametersSequence = imaResultDataFields["parameters/sequence"] if "parameters/sequence" in imaResultDataFields else None
            #parametersOrigin = imaResultDataFields["parameters/origin"] if "parameters/origin" in imaResultDataFields else None
    
            # Manually added data
            scannerManufacturer = "Siemens"
            scannerManufacturerModelName = "Vision"
            scannerMagneticFieldStrength = 1.5
            conversionSoftware = "dcm2nii"
            conversionSoftwareVersion = "2013.06.12"
    
            # create a BIDS sidecar json file from the data we got
            json_contents = {}
    
            # scanner info
            json_contents['Manufacturer'] = scannerManufacturer
            json_contents['ManufacturersModelName'] = scannerManufacturerModelName
            json_contents['MagneticFieldStrength'] = scannerMagneticFieldStrength
    
            # scan-specific info
            #json_contents['AcquisitionTime'] = ""
            #json_contents['SeriesNumber'] = ""
            json_contents['EchoTime'] = parametersTe
            json_contents['RepetitionTime'] = parametersTr
            json_contents['FlipAngle'] = parametersFlip
    
            json_contents['ConversionSoftware'] = conversionSoftware
            json_contents['ConversionSoftwareVersion'] = conversionSoftwareVersion
    
            # output BIDS sidecar file, make sure the name is the same as the .nii.gz output filename
    
            # get base of bidsname (get name from name.nii.gz) to construct json filename
            with open(os.path.join(scanBidsDir, bidsname) + ".json", "w+") as outfile:
                json.dump(json_contents, outfile, indent=4)
    
        print 'Done.'
    
        # Move imaging to image directory
        for f in os.listdir(scanBidsDir):
            if "nii" in f:
                os.rename(os.path.join(scanBidsDir, f), os.path.join(scanImgDir, f))
    
        # Check number of files in image directory, if more than one assume multiple echoes
        numechoes = len(os.listdir(scanImgDir))  # multiple .nii.gz files will be generated by dcm2niix if there are multiple echoes
        if numechoes > 1:
            # Loop through set of folders (IMG and BIDS)
            for dir in (scanImgDir, scanBidsDir):
                # Get sorted list of files
                multiple_echoes = sorted(os.listdir(dir))
    
                # Divide length of file list by number of echoes to find out how many files in each echo
                # (Multiband DWI would have BVEC, BVAL, and JSON in BIDS dir for each echo)
                filesinecho = len(multiple_echoes) / numechoes
    
                echonumber = 1
                filenumber = 1
    
                # Rename files
                for echo in multiple_echoes:
                    splitname = echo.split("_")
    
                    # Locate run if present in BIDS name
                    runstring = [s for s in splitname if "run" in s]
    
                    if runstring != []:
                        runindex = splitname.index(runstring[0])
                        splitname.insert(runindex, "echo-" + str(echonumber))  # insert where run is (will displace run to later position)
                    else:
                        splitname.insert(-1, "echo-" + str(echonumber))  # insert right before the data type
    
                    # Remove the "a" or other character from before the .nii.gz if not on the first echo
                    if (echonumber > 1):
                        ending = splitname[-1].split(".")
                        cleanedtype = ending[0][:-1]
                        ending[0] = cleanedtype
                        cleanedname = ".".join(ending)
                        splitname[-1] = cleanedname
    
                    # Rejoin name
                    echoname = "_".join(splitname)
    
                    # Do file rename
                    os.rename(os.path.join(dir, echo), os.path.join(dir, echoname))

                    # Add to scansTsv
                    scansTsv.append([os.path.join(bidssubdir, echoname), session, scanid])
    
                    # When file count rolls over increment echo and continue
                    if filenumber == filesinecho:
                        echonumber += 1
                        filenumber = 1  # restart count for new echo
    
                    # Increment file count each time one is renamed
                    filenumber += 1
        else:
            # Add to scansTsv
            scansTsv.append([bidsfilename, session, scanid])

        ##########
        # Upload results
        print
        print 'Preparing to upload files for scan %s.' % scanid
    
        # If we have a NIFTI resource and we've reached this point, we know overwrite=True.
        # We should delete the existing NIFTI resource.
        if hasNifti:
            print "Scan %s has a preexisting NIFTI resource. Deleting it now." % scanid
    
            try:
                queryArgs = {}
                if workflowId is not None:
                    queryArgs["event_id"] = workflowId
                r = xnatSession.httpsess.delete(host + "/data/experiments/%s/scans/%s/resources/NIFTI" % (session, scanid), params=queryArgs)
                r.raise_for_status()
    
                r = xnatSession.httpsess.delete(host + "/data/experiments/%s/scans/%s/resources/BIDS" % (session, scanid), params=queryArgs)
                r.raise_for_status()
            except (requests.ConnectionError, requests.exceptions.RequestException) as e:
                print "There was a problem deleting"
                print "    " + str(e)
                print "Skipping upload for scan %s." % scanid
                continue
    
        # Uploading
        print 'Uploading files for scan %s' % scanid
        queryArgs = {"format": "NIFTI", "content": "NIFTI_RAW", "tags": "BIDS"}
        if workflowId is not None:
            queryArgs["event_id"] = workflowId
        if uploadByRef:
            queryArgs["reference"] = os.path.abspath(scanImgDir)
            r = xnatSession.httpsess.put(host + "/data/experiments/%s/scans/%s/resources/NIFTI/files" % (session, scanid), params=queryArgs)
        else:
            queryArgs["extract"] = True
            (t, tempFilePath) = tempfile.mkstemp(suffix='.zip')
            zipdir(dirPath=os.path.abspath(scanImgDir), zipFilePath=tempFilePath, includeDirInZip=False)
            files = {'file': open(tempFilePath, 'rb')}
            r = xnatSession.httpsess.put(host + "/data/experiments/%s/scans/%s/resources/NIFTI/files" % (session, scanid), params=queryArgs, files=files)
            os.remove(tempFilePath)
        r.raise_for_status()
    
    
        queryArgs = {"format": "BIDS", "content": "BIDS", "tags": "BIDS"}
        if workflowId is not None:
            queryArgs["event_id"] = workflowId
        if uploadByRef:
            queryArgs["reference"] = os.path.abspath(scanBidsDir)
            r = xnatSession.httpsess.put(host + "/data/experiments/%s/scans/%s/resources/BIDS/files" % (session, scanid), params=queryArgs)
        else:
            queryArgs["extract"] = True
            (t, tempFilePath) = tempfile.mkstemp(suffix='.zip')
            zipdir(dirPath=os.path.abspath(scanBidsDir), zipFilePath=tempFilePath, includeDirInZip=False)
            files = {'file': open(tempFilePath, 'rb')}
            r = xnatSession.httpsess.put(host + "/data/experiments/%s/scans/%s/resources/BIDS/files" % (session, scanid), params=queryArgs, files=files)
            os.remove(tempFilePath)
        r.raise_for_status()
    
        ###########
        ## Clean up input directory
        #print
        #print 'Cleaning up %s directory.' % scanDicomDir
        #for f in os.listdir(scanDicomDir):
        #    os.remove(os.path.join(scanDicomDir, f))
        #os.rmdir(scanDicomDir)
    
        print
        print 'All done with image conversion.'
    
    ##########
    # Generate session-level metadata files
    previouschanges = ""
    
    # Remove existing files if they are there
    print "Check for presence of session-level BIDS data"
    r = get(host + "/data/experiments/%s/resources" % session, params={"format": "json"})
    sessionResources = r.json()["ResultSet"]["Result"]
    print 'Found resources %s.' % ', '.join(res["label"] for res in sessionResources)
    
    # Do initial checks to determine if session-level BIDS metadata is present
    hasSessionBIDS = any([res["label"] == "BIDS" for res in sessionResources])
    
    if hasSessionBIDS:
        print "Session has preexisting BIDS resource. Deleting previous BIDS metadata if present."
    
        # Consider making CHANGES a real, living changelog
        # r = get( host + "/data/experiments/%s/resources/BIDS/files/CHANGES"%(session) )
        # previouschanges = r.text
        # print previouschanges
    
        try:
            queryArgs = {}
            if workflowId is not None:
                queryArgs["event_id"] = workflowId
    
            r = xnatSession.httpsess.delete(host + "/data/experiments/%s/resources/BIDS" % session, params=queryArgs)
            r.raise_for_status()
            uploadSessionBids = True
        except (requests.ConnectionError, requests.exceptions.RequestException) as e:
            print "There was a problem deleting"
            print "    " + str(e)
            print "Skipping upload for session-level files."
            uploadSessionBids = False
    
        print "Done"
        print ""
    
    # Fetch metadata from project
    print "Fetching project {} metadata".format(project)
    rawprojectdata = get(host + "/data/projects/%s" % project, params={"format": "json"})
    projectdata = rawprojectdata.json()
    print "Got project metadata\n"
    
    # Build dataset description
    print "Constructing BIDS data"
    dataset_description = OrderedDict()
    dataset_description['Name'] = project
    
    dataset_description['BIDSVersion'] = BIDSVERSION
    
    # License- to be added later on after discussion of sensible default options
    # dataset_description['License'] = None
    
    # Compile investigators and PI into names list
    invnames = []
    invfield = [x for x in projectdata["items"][0]["children"] if x["field"] == "investigators/investigator"]
    print str(invfield)
    
    if invfield != []:
        invs = invfield[0]["items"]
    
        for i in invs:
            invnames.append(" ".join([i["data_fields"]["firstname"], i["data_fields"]["lastname"]]))
    
    pifield = [x for x in projectdata["items"][0]["children"] if x["field"] == "PI"]
    
    if pifield != []:
        pi = pifield[0]["items"][0]["data_fields"]
        piname = " ".join([pi["firstname"], pi["lastname"]])
    
        if piname in invnames:
            invnames.remove(piname)
    
        invnames.insert(0, piname + " (PI)")
    
    if invnames != []:
        dataset_description['Authors'] = invnames
    
    # Other metadata - to be added later on
    # dataset_description['Acknowledgments'] = None
    # dataset_description['HowToAcknowledge'] = None
    # dataset_description['Funding'] = None
    # dataset_description['ReferencesAndLinks'] = None
    
    # Session identifier
    dataset_description['DatasetDOI'] = host + '/data/experiments/' + session
    
    # Upload
    queryArgs = {"format": "BIDS", "content": "BIDS", "tags": "BIDS", "inbody": "true"}
    if workflowId is not None:
        queryArgs["event_id"] = workflowId
    
    r = xnatSession.httpsess.put(host + "/data/experiments/%s/resources/BIDS/files/dataset_description.json" % session, json=dataset_description, params=queryArgs)
    r.raise_for_status()
    
    # Generate CHANGES
    changes = "1.0 " + time.strftime("%Y-%m-%d") + "\n\n - Initial release."
    
    # Upload
    h = {"content-type": "text/plain"}
    r = xnatSession.httpsess.put(host + "/data/experiments/%s/resources/BIDS/files/CHANGES" % session, data=changes, params=queryArgs, headers=h)
    r.raise_for_status()

    # Generate scans.tsv
    tsvname = '{}scans.tsv'.format(base)
    tsvfile = os.path.join(builddir, tsvname)
    with open(tsvfile, 'w') as tsv:
        writer = csv.writer(tsv, delimiter='\t')
        writer.writerow(['filename', 'xnat_session_id', 'xnat_scan_id'])
        for row in scansTsv:
            writer.writerow(row)

    queryArgs = {"format": "BIDS", "content": "BIDS", "tags": "BIDS"}
    if workflowId is not None:
        queryArgs["event_id"] = workflowId
    files = {'file': open(tsvfile, 'rb')}
    r = xnatSession.httpsess.put(host + "/data/experiments/%s/resources/BIDS/files/%s" % (session, tsvname), params=queryArgs, files=files)
    r.raise_for_status()
    
    print 'All done with session-level metadata.'

# All done
finally:
    xnatSession.close_httpsession()
