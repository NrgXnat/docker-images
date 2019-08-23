#!/usr/bin/python3
import os , sys, errno
import math
import time, scipy.misc
import tensorflow as tf
import re
import requests
import numpy as np
import glob2,os
from collections import Counter
from itertools import repeat, chain
import warnings
try:
    import pydicom as dicom
except ImportError:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import dicom






# Read Images info and XNAT info
pathjpg = sys.argv[1]  # adress of jpg images
pathdicom = sys.argv[2]  # adress of dicom images
sessionid = sys.argv[3]
Scan = sys.argv[4]
XNAT_HOST = sys.argv[5]
XNAT_USER = sys.argv[6]
XNAT_PASS = sys.argv[7]
File_Number=sys.argv[8]
all_header_jpgfiles = glob2.glob(os.path.join(pathjpg,'**/*.jpg'))
all_header_dicomfiles = glob2.glob(os.path.join(pathdicom,'**/*'))













#Get Dicom metadata and relevant features
ds = dicom.read_file(all_header_dicomfiles[0])
try:
    Image_Type=str(ds.ImageType).lower()
except (AttributeError, IndexError) as err:
    Image_Type="NAN"
try:
    Modality=str(ds.Modality).lower()
except:
    Modality="NAN"

try:
    Series_Description=str(ds.SeriesDescription).lower().replace("image","")
except (AttributeError, IndexError) as err:
    Series_Description="NAN"

Number_Slices=int(File_Number)
try:
    Angio=str(ds.AngioFlag).lower()
except (AttributeError, IndexError) as err:
    Angio="NAN"

#
#try:
#    ContrastBolusAgent=ds.ContrastBolusAgent
#except (AttributeError, IndexError) as err:
#    ContrastBolusAgent="NAN"
#
#if (ContrastBolusAgent!="NAN"):
#    Contrast="Gad_"
#else:
#    Contrast=""


try:
    ContrastBolusAgent=ds.ContrastBolusAgent
except (AttributeError, IndexError) as err:
    ContrastBolusAgent="NAN"

try:
    Volume=ds.ContrastBolusVolume
except (AttributeError, IndexError, KeyError) as err:
    Volume="NAN"


if (ContrastBolusAgent!="NAN"):
    if (Volume!="NAN"):
        if(Volume==0 and (Series_Description.find("gad") == -1) and (Series_Description.find("gd") == -1)):
            Contrast=""
        else:
            Contrast="ce-Gad_"
    else:
        if(len(ContrastBolusAgent)!=0 or (Series_Description.find("gad") != -1) or (Series_Description.find("gd") != -1)):
            Contrast="ce-Gad_"
        else:
            Contrast=""
else:
    Contrast=""



def processInput(i):
    # change this as you see fit
    jpgimage_path = all_header_jpgfiles[i]
    Size=len(jpgimage_path)
    # Unpersists graph from file
    with tf.gfile.FastGFile("./retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')
    # Read in the image_data
    jpgimage_data = tf.gfile.FastGFile(jpgimage_path, 'rb').read()
    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, \
                               {'DecodeJpeg/contents:0': jpgimage_data})
        List=(-predictions[0]).argsort()[:2]
    return List













#Image classification
if (((Image_Type.find("derived") != -1)!=True) and (Image_Type.find("primary") != -1)):
    # #classification based on pixel info
    results=[]
    inputs=range(0,len(all_header_jpgfiles))
    for i in inputs:
        results.append(processInput(i))
    label_lines = [line.rstrip() for line in tf.gfile.GFile("./retrained_labels.txt")]
    Label_P=[]
    if (len(results)!=0):
        for i in range(2):
            Label_P.append(label_lines[results[0][i]])

#    print("Pixel-based classification is ", Label_P)

    #classification based on dicom header
    Label_H=[]
    if (any(x in Series_Description for x in ['scout'])):
        Label_H.append('Scout')
    if (((Series_Description.find("loc") != -1) and (Series_Description.find("block") == -1) and (Series_Description.find("location") == -1)) or ((Number_Slices<=3) and (len(results)!=0))):
        Label_H.append('Localizer')
    if (any(x in Series_Description for x in ['flash','ge','gre']) and Series_Description.find("average") == -1 and Series_Description.find("mprage") == -1):
        Label_H.append('FLASH')
    if any(x in Series_Description for x in ['dif','dwi','dti','dbsi','tracew','colfa','tensor','fa','adc','resolve','ansio','aniso','iso']):
        Label_H.append('DWI')
    if any(x in Series_Description for x in ['swi','swan']):
        Label_H.append('SWI')
    if ((Series_Description.find("t2") != -1) and ((Series_Description.find("*") != -1) or (Series_Description.find("star") != -1))):
        Label_H.append('T2star')
    if any(x in Series_Description for x in ['bold','fmri','rest']):
        Label_H.append('Bold')
    if any(x in Series_Description for x in ['asl']):
        Label_H.append('ASL')
    if any(x in Series_Description for x in ['dsc','dce','perf']):
        Label_H.append('Perfusion')
    if (any(x in Series_Description for x in ['angio','tof','exorcist','tumbler']) or Angio=='y'):
        Label_H.append('Angio')
    if (any(x in Series_Description for x in ['mip'])):
        Label_H.append('minIP')
    if any(x in Series_Description for x in ['tse','fse']):
        Label_H.append('TSE')
    if any(x in Series_Description for x in ['flair']):
        Label_H.append('Flair')
    if (Series_Description.find("map") != -1) and (Series_Description.find("field") != -1):
        Label_H.append('Fieldmap')
    if (any(x in Series_Description for x in ['mag'])):
        Label_H.append('part-Mag_GRE')
    if (any(x in Series_Description for x in ['pha'])):
        Label_H.append('part-Phase_GRE')
    if (any(x in Series_Description for x in ['t1','mpr','fspgr']) and (Series_Description.find("t2") == -1) and (not any(x in Series_Description for x in ['t10','t11','t12','t13','t14','t15','t16','t17','t18','t19']))):
        Label_H.append('T1w')
    if (any(x in Series_Description for x in ['t2']) and (not any(x in Series_Description for x in ['t20','t21','t22','t23','t24','t25','t26','t27','t28','t29']))):
        Label_H.append('T2w')


#    print("Text-based classification is ", Label_H)





    #Combine Classification results
    if((len(Label_H)==0) and (len(Label_P)==0)):
        Label='Unknown'
    elif((len(Label_H)==0) and (len(Label_P)!=0)):
        Label=Label_P[0]
    elif((len(Label_H)!=0) and (len(Label_P)==0)):
        Label=Label_H[0]
    else:
        if(len(Label_H)==1):
            Label=Label_H[0]
        elif('Scout' in Label_H):
            Label='Scout'
        elif('Localizer' in Label_H):
            Label='Localizer'
        elif('Perfusion' in Label_H):
            Label='Perfusion'
        else:
            for k in range(len(Label_P)):
                if Label_P[k] in Label_H:
                    Label=Label_P[k]
                    break
            Label=Label_H[0]
else:
    Label="Derived"


if Label!="Derived":
    Label=Contrast+Label

print("\nSetting label for %s %s to %s\n" % (sessionid, Scan, Label))

# Change value of data type
if (Modality.find("mr") != -1):
    os.system("curl -k -L -u "+XNAT_USER+":"+XNAT_PASS+" '"+XNAT_HOST+"/data/experiments/"+sessionid+"/scans/"+Scan+"?xsiType=xnat:mrScanData&xnat:imageScanData/series_class="+Label+"'"+ " -X PUT")
    # s = requests.Session()
    # s.auth = (XNAT_USER, XNAT_PASS)
    # r = s.put(XNAT_HOST+"/data/experiments/"+sessionid+"/scans/"+Scan+"/files",params={"xsiType": "xnat","mrScanData&xnat:imageScanData/series_class": Label})
    # r.close()
else:
    os.system("curl -k -L -u "+XNAT_USER+":"+XNAT_PASS+" '"+XNAT_HOST+"/data/experiments/"+sessionid+"/scans/"+Scan+"?xsiType=xnat:mrScanData&xnat:imageScanData/series_class=Unknown"+"'"+ " -X PUT")
    # s = requests.Session()
    # s.auth = (XNAT_USER, XNAT_PASS)
    # r = s.put(XNAT_HOST+"/data/experiments/"+sessionid+"/scans/"+Scan+"/files",params={"xsiType": "xnat","mrScanData&xnat:imageScanData/series_class": "Unknown"}, headers={'Connection':'close'})

#os.system("curl -X PUT -u {}:{} -H 'Content-Type: application/json' -H 'Accept: */*' -d '[{}/archive/experiments/{}/scans/{}{}]' '{}/xapi/archive/catalogs/refresh'".format(XNAT_USER,XNAT_PASS,'"',sessionid,Scan,'"',XNAT_HOST))

