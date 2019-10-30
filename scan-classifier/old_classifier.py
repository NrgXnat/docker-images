import os , sys, errno, shutil, uuid
import pandas as pd
import numpy as np
import math
import time,scipy.misc
import glob2
import re
import requests
import gzip
import tensorflow as tf
try:
    import pydicom as dicom
except ImportError:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import dicom

# Get directory of scans
inputDir = sys.argv[1]
workingDir = sys.argv[2]
Session_ID = sys.argv[3]
Scans = sys.argv[4]
XNAT_HOST = os.environ['XNAT_HOST']
XNAT_USER = os.environ['XNAT_USER']
XNAT_PASS = os.environ['XNAT_PASS']

regex = re.compile(r'.*\.xml$')
for Scan_ID in Scans.split():
    print("Inspecting scan %s" % Scan_ID)
    scanDir = os.path.join(inputDir, "SCANS", Scan_ID, "DICOM")
    # List of DICOM files (excludes catalog xml)
    dicomFiles = [fl for fl in glob2.iglob(os.path.join(scanDir, "*"), recursive=True) if not regex.match(fl)]
    if len(dicomFiles) == 0:
        sys.stderr.write("ERROR: No DICOM images found for scan " + Scan_ID)
        continue
    scanWorkDir = os.path.join(workingDir, Scan_ID)
    rawDir = os.path.join(scanWorkDir, 'RAW')
    os.makedirs(rawDir)
    jpgDir = os.path.join(scanWorkDir, 'JPG' )
    os.makedirs(jpgDir)
    M = math.ceil(len(dicomFiles)*0.7)
    Li = max(0,M-1)
    Ui = min(len(dicomFiles), Li)
    #for i in range(Li,Ui):
    #    selectedDicomFiles.append(dicomFiles[i])
    #    shutil.copy(dicomFiles[i], rawDir)
    #cmd = '%s %s %s' % ('for f in $(find ', rawDir +' -type f',' >/dev/null 2>&1);do python2 ./DecompressDCM.py $f $f ; done')
    selectedDicom = dicomFiles[Ui]
    #shutil.copy(selectedDicom, rawDir)
    image = os.path.join(rawDir, os.path.basename(selectedDicom))
    cmd = '%s %s %s' % ('python2 ./DecompressDCM.py ', selectedDicom, image)
    print(cmd)
    os.system(cmd)
    jpgName = os.path.splitext(os.path.basename(image))[0] + '.jpg'
    print("Converting %s to %s" % (image, jpgName))
    image_array = dicom.read_file(image).pixel_array
    scipy.misc.toimage(image_array, high = 255, low = 0, cmin=0.0, cmax=4096).save(os.path.join(jpgDir, jpgName))
    #images = glob2.glob(os.path.join(rawDir, '*'))
    #for image in images:
    #    jpgName = os.path.splitext(os.path.basename(image))[0] + '.jpg'
    #    print("Converting %s to %s" % (image, jpgName))
    #    image_array = dicom.read_file(image).pixel_array
    #    scipy.misc.toimage(image_array, high = 255, low = 0, cmin=0.0, cmax=4096).save(os.path.join(jpgDir, jpgName))
    File_Number = str(len(dicomFiles))
    cmd = '%s %s %s %s %s %s %s %s %s' % ('python label_probability.py', jpgDir, rawDir, Session_ID, Scan_ID, XNAT_HOST, XNAT_USER, XNAT_PASS, File_Number)
    print(cmd.replace(XNAT_PASS, "******"))
    os.system(cmd)
    os.system('%s %s' % ('rm -rf ', scanWorkDir))
