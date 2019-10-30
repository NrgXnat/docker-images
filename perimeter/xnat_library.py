#!/usr/bin/env python

import numpy as np
import zipfile
import xml.etree.ElementTree as ET
import re
import os
import tifffile
from nibabel.testing import data_path
import nibabel as nib
from PIL import Image
from pyxnat import Interface

def fread(fid, nelements, dtype):
    #Equivalent to Matlab fread function
    if dtype is np.str:
        dt = np.uint8  # WARNING: assuming 8-bit ASCII for np.str!
    else:
        dt = dtype
    data_array = np.fromfile(fid, dt, nelements)
    return data_array

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    # Turn a string into a list of string and number chunks.  "z23a" -> ["z", 23, "a"]    
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    #Sort the given list in the way that humans expect.    
    l.sort(key=alphanum_key)

#Read in single U16 image
class ReadU16:
    def __init__(self, fid):        
        fileID = open(fid)
        self.fileSize = fread(fileID,1,'uint32')[0]
        self.fileVersion = fread(fileID,1,'uint32')[0]
        self.imageFactor = fread(fileID,1,'uint32')[0]
        self.widthPixels = fread(fileID,1,'uint32')[0]
        self.heightPixels = fread(fileID,1,'uint32')[0]
        self.caseId = fread(fileID,1,'uint32')[0]
        self.scanId = fread(fileID,1,'uint32')[0]
        self.sliceNumber = fread(fileID,1,'uint32')[0]
        self.numCellsAdded = fread(fileID,1,'uint32')[0]
        self.numCellsExpected = fread(fileID,1,'uint32')[0]
        self.serialNumber = fread(fileID,1,'uint64')[0]
        self.imgWidth = fread(fileID,1,'float32')[0]
        self.imgHeight = fread(fileID,1,'float32')[0]  
        self.glassHeightMm = fread(fileID,1,'float32')[0]
        self.xLocationMm = fread(fileID,1,'float32')[0]
        self.yLocationMm = fread(fileID,1,'float32')[0]
        self.indexOfRefraction = fread(fileID,1,'float32')[0]
        self.probeTiltAngleX = fread(fileID,1,'float32')[0]
        self.probeTiltAngleY = fread(fileID,1,'float32')[0]
        self.referenceArmIntensity = fread(fileID,1,'float32')[0]    
        self.imageData = fread(fileID,self.fileSize,"uint16")
        self.imageData = np.reshape(self.imageData,(self.heightPixels,self.widthPixels))
        fileID.close()        
        
#Create volume given a folder location
class MakeOTISvolume:
    def __init__(self, inputFolder, inputfiletype, clipheight=0, clipdepth=512, lowerWL = 50, upperWL=160):
        print("MakeOTISvolume: listing {}".format(inputFolder))
        flist = []
        for i in os.listdir(inputFolder):        
            if (i[-3:] == inputfiletype):            
                flist.append(i)
            sort_nicely(flist)
        print("MakeOTISvolume: reading {} as template".format(flist[1]))
        temp = ReadU16(os.path.join(inputFolder, flist[1]))
        self.bScanSpacing = temp.yLocationMm*1000
        self.pixelHeight = temp.imgHeight/temp.heightPixels*1.4*1000
        self.pixelWidth = temp.imgWidth/temp.widthPixels*1000
        self.caseId = temp.caseId
        self.scanId = temp.scanId                       
        self.data = np.zeros((len(flist), clipdepth-clipheight, temp.widthPixels),dtype=np.uint8)
        count = 0
        if (self.data.shape[2]>0):
            for i in flist:
                print("MakeOTISvolume: reading {}".format(i))
                temp = ReadU16(os.path.join(inputFolder,i))
                temp.imageData = (temp.imageData/255)[clipheight:clipdepth].astype(np.uint8)
                temp.imageData = np.clip(temp.imageData, lowerWL, upperWL)
                temp.imageData = (temp.imageData-lowerWL)*(255/(upperWL-lowerWL))               
                self.data[count,:,:] = temp.imageData.astype(np.uint8)
                count += 1   
        print("MakeOTISvolume: complete")
        
#Updated for nifti/imageJ
def convertOTIS(inputFolder, outputdir, inputfiletype = "u16", outputfiletype = 'gz', clipheight = 0, clipdepth = 512, lowerWL = 50, upperWL=160):
    print("convertOTIS: converting data in {} to {} in {}".format(inputFolder, outputfiletype, outputdir))
    volume = MakeOTISvolume(inputFolder, inputfiletype, clipheight, clipdepth)       
    print("convertOTIS: saving file")
    if (outputfiletype == "tif"):
        y,z,x = volume.data.shape 
        volume.data.shape = 1, y, 1, z, x, 1
        fname = os.path.join(outputdir, "P%06d_S%02d.tif" %(volume.caseId, volume.scanId))
        tifffile.imsave(fname, volume.data, imagej=True, resolution=(1./volume.pixelWidth, 1./volume.pixelHeight), metadata={'spacing': volume.bScanSpacing, 'unit': 'um'})
    elif (outputfiletype == "gz"):                
        volume.data = np.rot90(volume.data, 1, axes=(0,2)) #Rotation is used to make the orientation consistent with ImageJ
        pixDimR = list([volume.pixelWidth, volume.pixelHeight, volume.bScanSpacing])         
        img = nib.Nifti1Image(volume.data, np.eye(4))
        img.header.get_xyzt_units()
        img.header.set_zooms(pixDimR)         
        aff = img.header.get_qform()
        aff[[0,2]]=-aff[[2,0]] #two lines changes the orientation from LPI to PSR (for normal viewing in ITK-SNAP)
        aff[[1,2]]=-aff[[2,1]]      
        img.header.set_qform(affine=aff)        
        fname = os.path.join(outputdir, "P%06d_S%02d.nii.gz" %(volume.caseId, volume.scanId))
        img.to_filename(fname)
    print("convertOTIS: wrote {}".format(fname))
    print("convertOTIS: complete")

def convertOTIS2XNAT(inputFolder, outNifti, outTiff, host, user, passwd, sessionId, scanId, inputfiletype = "u16", clipheight = 0, clipdepth = 512):
    print("convertOTIS: converting data in {} to nifti/tif/jpg", inputFolder)
    volume = MakeOTISvolume(inputFolder, inputfiletype, clipheight, clipdepth)
    print("convertOTIS: saving files")
    name = "P%06d_S%02d" %(volume.caseId, volume.scanId)
    xnat = Interface(server=host, user=user, password=passwd)
    # we need to load the scan such that the URI contains proj & subj so that file uploading works
    exp = xnat.select.experiment(sessionId)
    subId = exp.attrs.get('xnat:imageSessionData/SUBJECT_ID')
    projId = exp.attrs.get('project')
    scan = xnat.select.project(projId).subject(subId).experiment(sessionId).scan(scanId)
    for outputfiletype in ["tif", "gz"]:
        if (outputfiletype == "tif"):
            y,z,x = volume.data.shape
            volume.data.shape = 1, y, 1, z, x, 1
            fname = os.path.join(outTiff, "%s.tif" % name)
            tifffile.imsave(fname, volume.data, imagej=True, resolution=(1./volume.pixelWidth, 1./volume.pixelHeight), metadata={'spacing': volume.bScanSpacing, 'unit': 'um'})
            #revert
            volume.data.shape = y,z,x
            nimg = 49
            im = Image.open(fname)
            snapshot = np.zeros((896,896))
            slices = np.linspace(0, im.n_frames-1, num=nimg, dtype=int)
            for i in range(slices.shape[0]):
                row = i // 7
                col = i % 7
                im.seek(slices[i])
                snapshot[128*row:128*(row+1),128*col:128*(col+1)] = np.array(im.resize((128,128)))
            f = os.path.join("/tmp", "%s.jpg" % name)
            snap = Image.fromarray(snapshot).convert("L")
            snap.save(f)
            scan.resource("SNAPSHOTS").file("%s.jpg" % name).insert(f, content="ORIGINAL", format="JPG")
            f = os.path.join("/tmp", "%s_t.jpg" % name)
            snap.resize((448,448)).save(f)
            scan.resource("SNAPSHOTS").file("%s_t.jpg" % name).insert(f, content="THUMBNAIL", format="JPG")
        elif (outputfiletype == "gz"):
            volume.data = np.rot90(volume.data, 1, axes=(0,2)) #Rotation is used to make the orientation consistent with ImageJ
            pixDimR = list([volume.pixelWidth, volume.pixelHeight, volume.bScanSpacing])
            img = nib.Nifti1Image(volume.data, np.eye(4))
            img.header.get_xyzt_units()
            img.header.set_zooms(pixDimR)
            aff = img.header.get_qform()
            aff[[0,2]]=-aff[[2,0]] #two lines changes the orientation from LPI to PSR (for normal viewing in ITK-SNAP)
            aff[[1,2]]=-aff[[2,1]]
            img.header.set_qform(affine=aff)
            fname = os.path.join(outNifti, "%s.nii.gz" % name)
            img.to_filename(fname)
        print("convertOTIS: wrote {}".format(fname))
    print("convertOTIS: adding metadata to XNAT")
    fields = volume.__dict__
    xnatJson = {}
    for fieldName in fields.keys():
        if fieldName == "data":
            continue
        xnatJson["xnat:imageScanData/parameters/addParam[name=%s]/addField" % fieldName] = str(fields[fieldName])
    scan.attrs.mset(xnatJson)
    print("convertOTIS: complete")
        
#GENERATE FULL FILESRUCTURE FROM THE OTIS DATA
def fileGen(folderID, ftype1 = 'P0', ftype2 = "S", ftype3 = 'u16'):
    flist = []
    xcount = 0
    for x in os.listdir(folderID):
        if (x[0:2] == ftype1):
            ycount = 1
            flist.append([x])            
            for y in os.listdir(folderID+x+"//"):
                if (y[0] == ftype2):
                    flist[xcount].append([y])
                    flist[xcount][ycount].append([])
                    for z in os.listdir(folderID + x + "//" + y + "//"):
                        if (z[-3:] == ftype3):
                            flist[xcount][ycount][1].append(z)
                    sort_nicely(flist[xcount][ycount][1])
                    ycount += 1
            xcount +=1 
    return(flist)    
        
#Batch convert an entire directory, also checks output to make sure output file doesn't exist already
def batchConvertOTIS(homedir, outputdir, inputfiletype = "u16", outputfiletype = 'gz', clipheight = 0, clipdepth = 512, startindex = 0):
    flist = fileGen(homedir)
    for i in range (startindex, len(flist)):
        for j in range (1,len(flist[:][i])):        
            fileCheck = os.path.join(outputdir, flist[i][0] + '_' + flist[i][j][0])
            if not (os.path.isfile(fileCheck + ".tif") or os.path.isfile(fileCheck + ".nii.gz")):
                print (flist[i][0] + " " + flist[i][j][0] + " => %d" %len(flist[i][j][1][:]))
                if (len(flist[i][j][1][:])>0):
                    inputdir = os.path.join(homedir, flist[i][0], flist[i][j][0])
                    convertOTIS(inputdir, outputdir, inputfiletype, outputfiletype, clipheight, clipdepth)
                    
                    
# class ReadOCT:
#         def __init__(self, fid): 
#             zip_ref = zipfile.ZipFile(fileloc, 'r')    
#             root = ET.parse(zip_ref.open('Header.xml','r')).getroot()
#             acquisitionMode = root.find("MetaInfo/AcquisitionMode").text
#             if (acquisitionMode == "Mode2D"):
                
# class ReadP16:
#     def __init__(self, fid):        
#         print (" ")


