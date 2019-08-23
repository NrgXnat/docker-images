import os, sys, errno
#import subprocess, shutil
import numpy
import math
import time,scipy.misc
import glob2
import tensorflow as tf
from joblib import Parallel, delayed
import multiprocessing
import re
import numpy as np
import glob2,os
from joblib import Parallel, delayed
import multiprocessing
import os
import numpy
from matplotlib import pyplot, cm
from xlwt import Workbook



wb = Workbook()



# Read Image Pathes
#MainDir = sys.argv[1]  # adress of jpg images
#MainDir="./WUSTL_170_09162015_1920_FU1"

#Session = MainDir.split('/')[-1]
#print(Session)


# Create a workbook and add a worksheet.
#workbook = xlsxwriter.Workbook(Session +'.xlsx')
worksheet1 = wb.add_sheet('BIDS Labels')
worksheet1.write(0,0, 'Session')
worksheet1.write(0,1, 'Scan')
worksheet1.write(0,2, 'Image Type')
worksheet1.write(0,3, 'Series Description')
worksheet1.write(0,4, 'Folder')
worksheet1.write(0,5, 'Contrast Type')
worksheet1.write(0,6, 'BIDS label')
worksheet2 = wb.add_sheet('Derived Scan Labels')
worksheet2.write(0,0, 'Session')
worksheet2.write(0,1, 'Scan')
worksheet2.write(0,2, 'Image Type')
worksheet2.write(0,3, 'Series Description')
worksheet2.write(0,4, 'Folder')
worksheet2.write(0,5, 'Contrast Type')
worksheet2.write(0,6, 'Scan label')
worksheet2.write(0,7, 'Secondary Type')


wb.save('ScanClassification.xls')
