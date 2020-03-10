import os, sys, errno
import math
import scipy.misc
import tensorflow as tf
import re
import glob
from collections import Counter
from itertools import repeat, chain
import warnings
import pydicom as dicom

def predictFromPixelData(image, basename, jpgDir):
    # Save as jpg
    jpgFile = os.path.join(jpgDir, basename + ".jpg")
    print("Converting dcm to %s" % jpgFile)
    scipy.misc.toimage(image, high = 255, low = 0, cmin=0.0, cmax=4096).save(jpgFile)

    # Unpersists graph from file
    with tf.gfile.FastGFile("./retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    # Read in the image_data
    with tf.gfile.FastGFile(jpgFile, 'rb') as f:
        jpgFileData = f.read()
    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, \
                               {'DecodeJpeg/contents:0': jpgFileData})
        prediction = (-predictions[0]).argsort()[:2]
    labels = [line.rstrip() for line in tf.gfile.GFile("./retrained_labels.txt")]
    labelP = []
    for i in range(2):
        labelP.append(labels[prediction[i]])

    print("Pixel-based classification is %s" % ' '.join(labelP))
    return labelP


def predictFromDcmHeader(ds, nDicomFiles, labelPIsEmpty):
    #classification based on dicom header
    try:
        seriesDesc=str(ds.SeriesDescription).lower().replace("image","")
    except (AttributeError, IndexError) as err:
        seriesDesc="NA"

    try:
        angio=str(ds.AngioFlag).lower()
    except (AttributeError, IndexError) as err:
        angio="NA"
    
    labelH=[]
    if (any(x in seriesDesc for x in ['scout'])):
        labelH.append('Scout')
    if (((seriesDesc.find("loc") != -1) and (seriesDesc.find("block") == -1) and (seriesDesc.find("location") == -1)) or (nDicomFiles <= 3 and labelPIsEmpty)):
        labelH.append('Localizer')
    if (any(x in seriesDesc for x in ['flash','ge','gre']) and seriesDesc.find("average") == -1 and seriesDesc.find("mprage") == -1):
        labelH.append('FLASH')
    if any(x in seriesDesc for x in ['dif','dwi','dti','dbsi','tracew','colfa','tensor','fa','adc','resolve','ansio','aniso','iso']):
        labelH.append('DWI')
    if any(x in seriesDesc for x in ['swi','swan']):
        labelH.append('SWI')
    if ((seriesDesc.find("t2") != -1) and ((seriesDesc.find("*") != -1) or (seriesDesc.find("star") != -1))):
        labelH.append('T2star')
    if any(x in seriesDesc for x in ['bold','fmri','rest']):
        labelH.append('Bold')
    if any(x in seriesDesc for x in ['asl']):
        labelH.append('ASL')
    if any(x in seriesDesc for x in ['dsc','dce','perf']):
        labelH.append('Perfusion')
    if (any(x in seriesDesc for x in ['angio','tof','exorcist','tumbler']) or angio=='y'):
        labelH.append('Angio')
    if (any(x in seriesDesc for x in ['mip'])):
        labelH.append('minIP')
    if any(x in seriesDesc for x in ['tse','fse']):
        labelH.append('TSE')
    if any(x in seriesDesc for x in ['flair']):
        labelH.append('Flair')
    if (seriesDesc.find("map") != -1) and (seriesDesc.find("field") != -1):
        labelH.append('Fieldmap')
    if (any(x in seriesDesc for x in ['mag'])):
        labelH.append('part-Mag_GRE')
    if (any(x in seriesDesc for x in ['pha'])):
        labelH.append('part-Phase_GRE')
    if (any(x in seriesDesc for x in ['t1','mpr','fspgr']) and (seriesDesc.find("t2") == -1) and (not any(x in seriesDesc for x in ['t10','t11','t12','t13','t14','t15','t16','t17','t18','t19']))):
        labelH.append('T1w')
    if (any(x in seriesDesc for x in ['t2']) and (not any(x in seriesDesc for x in ['t20','t21','t22','t23','t24','t25','t26','t27','t28','t29']))):
        labelH.append('T2w')

    print("Header-based classification is %s" % ' '.join(labelH))
    return labelH
    

def combineClassifications(labelP, labelH):
    #Combine Classification results
    if len(labelH) == 0 and len(labelP) == 0:
        overallLabel = 'Unknown'
    elif len(labelH) == 0 and len(labelP) > 0:
        overallLabel = labelP[0]
    elif len(labelH) > 0 and len(labelP) == 0:
        overallLabel = labelH[0]
    else:
        if len(labelH) == 1:
            overallLabel = labelH[0]
        elif 'Scout' in labelH:
            overallLabel='Scout'
        elif 'Localizer' in labelH:
            overallLabel='Localizer'
        elif 'Perfusion' in labelH:
            overallLabel='Perfusion'
        else:
            for k in range(len(labelP)):
                if labelP[k] in labelH:
                    return labelP[k]
            overallLabel=labelH[0]

    return overallLabel


def getContrastLabel(ds):
    try:
        contrastBolusAgent=ds.ContrastBolusAgent
    except (AttributeError, IndexError) as err:
        contrastBolusAgent="NA"
    
    try:
        volume=ds.ContrastBolusVolume
    except (AttributeError, IndexError, KeyError) as err:
        volume="NA"

    try:
        seriesDesc=str(ds.SeriesDescription).lower()
    except (AttributeError, IndexError) as err:
        seriesDesc="NA"
    
    if (contrastBolusAgent!="NA"):
        if (volume!="NA"):
            if(volume==0 and (seriesDesc.find("gad") == -1) and (seriesDesc.find("gd") == -1)):
                contrast=""
            else:
                contrast="ce-Gad_"
        else:
            if(len(contrastBolusAgent)!=0 or (seriesDesc.find("gad") != -1) or (seriesDesc.find("gd") != -1)):
                contrast="ce-Gad_"
            else:
                contrast=""
    else:
        contrast=""

    return contrast



def classify(dcmFile, jpgDir, scanId, nDicomFiles):
    # Read DICOM
    ds = dicom.read_file(dcmFile)

    try:
        modality=str(ds.Modality).lower()
    except:
        modality="NA"
    
    finalLabel = 'Unknown'
    if not "mr" in modality:
        print("%s is not an MR scan, classifying as '%s'" % (scanId, finalLabel))
    else:
        #Image classification
        try:
            imageType=str(ds.ImageType).lower()
        except (AttributeError, IndexError) as err:
            imageType="NA"
    
        if "primary" in imageType and not "derived" in imageType:
            # classification based on pixel info
            labelP = predictFromPixelData(ds.pixel_array, os.path.splitext(os.path.basename(dcmFile))[0], jpgDir)
            # classification based on dicom header
            labelH = predictFromDcmHeader(ds, nDicomFiles, len(labelP) == 0)
            # Combine
            overallLabel = combineClassifications(labelP, labelH)
            finalLabel = getContrastLabel(ds) + overallLabel
        else:
            finalLabel = "Derived"
            print("%s has ImageType='Derived', classifying as '%s'" % (scanId, finalLabel))

    return finalLabel
