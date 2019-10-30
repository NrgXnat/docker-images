#!/usr/bin/python
from xnat_library import convertOTIS2XNAT
import argparse

parser = argparse.ArgumentParser(description='Run PerimeterMed python functions')
parser.add_argument('--input', help='Input directory', default='/input')
parser.add_argument('--outputTiff', help='Output tiff directory', default='/output/tiff')
parser.add_argument('--outputNifti', help='Output nifti directory', default='/output/nifti')
parser.add_argument('--host', help='XNAT host', required=True)
parser.add_argument('--user', help='XNAT user', required=True)
parser.add_argument('--passwd', help='XNAT pass', required=True)
parser.add_argument('--sessionId', help='XNAT session ID', required=True)
parser.add_argument('--scanId', help='XNAT scan ID', required=True)

args = parser.parse_args()

convertOTIS2XNAT(args.input, args.outputNifti, args.outputTiff, args.host, args.user, args.passwd, args.sessionId, args.scanId)
