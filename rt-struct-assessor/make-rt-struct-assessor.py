#!/usr/bin/env python

'''make-rt-struct-assessor.py
Read in an RT-STRUCT DICOM file. Write out an icr:roiCollectionData assessor.

Usage:
    make-rt-struct-assessor.py SUBJECT_ID SESSION_ID SESSION_LABEL PROJECT DICOM_IN ASSESSOR_XML_OUT

Options:
    SUBJECT_ID                  ID of parent subject
    SESSION_ID                  ID of parent session
    SESSION_LABEL               Label of parent session
    PROJECT                     Project of parent session
    DICOM_IN                    Path to input RT-STRUCT DICOM file
    ASSESSOR_XML_OUT            Path to output XML file
'''

import os
import uuid
import pydicom
import datetime as dt
from docopt import docopt
from lxml.builder import ElementMaker
from lxml.etree import tostring as xmltostring

nsdict = {'xnat':'http://nrg.wustl.edu/xnat',
          'xsi':'http://www.w3.org/2001/XMLSchema-instance',
          'icr':'http://icr.ac.uk/icr'}

xnat_host = os.environ.get('XNAT_HOST', 'http://nrg.wustl.edu')
schema_location_template = "{0} {1}/xapi/schemas/{2}/{2}.xsd"
schema_location = schema_location_template.format(nsdict['xnat'], xnat_host, 'xnat') + \
                  schema_location_template.format(nsdict['icr'], xnat_host, 'roi')

def ns(namespace,tag):
    return "{%s}%s"%(nsdict[namespace], tag)

def get_dicom_header_value(line):
    left_bracket_idx = line.find('[')
    right_bracket_idx = line.find(']')
    if left_bracket_idx == -1 or right_bracket_idx == -1:
        return None
    return line[left_bracket_idx + 1:right_bracket_idx]

version = "1.0"
args = docopt(__doc__, version=version)
dicom_path = args.get('DICOM_IN')
subject_id = args.get("SUBJECT_ID")
session_id = args.get('SESSION_ID')
session_label = args.get('SESSION_LABEL')
project = args.get('PROJECT')
assessor_xml_path = args.get('ASSESSOR_XML_OUT')

print("Debug: args " + ", ".join("{}={}".format(name, value) for name, value in args.items()) + "\n")

print("Reading RT-STRUCT DICOM from {}".format(dicom_path))

tags = {
    'SOPInstanceUID': (0x0008, 0x0018),
    'StudyDate': (0x0008, 0x0020),
    'StudyTime': (0x0008, 0x0030),
    'StructureSetLabel': (0x3006, 0x0002),
    'ReferencedFrameOfReferenceSequence': (0x3006, 0x0010)
}

with open(dicom_path, 'rb') as f:
    dicom = pydicom.dcmread(f, specific_tags=tags.keys())

print(dicom)
print()

uid = dicom[tags['SOPInstanceUID']].value
name = dicom[tags['StructureSetLabel']].value
date =  dicom[tags['StudyDate']].value if tags['StudyDate'] in dicom else "yyyymmdd"
time_header = dicom[tags['StudyTime']].value if tags['StudyTime'] in dicom else "hhmmss"
time = time_header if '.' not in time_header else time_header[:time_header.index('.')]

# Need to get through a couple nested sequences to get to (0020, 000E)
# https://dicom.innolitics.com/ciods/rt-structure-set/structure-set/30060010/30060012/30060014/0020000e
# We need to go (3006, 0010) -> (3006, 0012) -> (3006, 0014) -> (0020, 000E)
referencedStudyUids = []
for referencedFrameOfReference in dicom[tags['ReferencedFrameOfReferenceSequence']]:
    for rtReferencedStudy in referencedFrameOfReference[(0x3006, 0x0012)]:
        for rtReferencedSeries in rtReferencedStudy[(0x3006, 0x0014)]:
            referencedStudyUids.append(rtReferencedSeries[(0x0020, 0x000E)].value)

assessor_label = "{}_RTSTRUCT_{}{}".format(session_label, date, "_" + time if time != "hhmmss" else "")
assessor_id = '{}_RTSTRUCT_{}'.format(session_id, uuid.uuid4())

assessorElements = [
    ('UID', uid),
    ('collectionType', 'RTSTRUCT'),
    ('subjectID', subject_id),
    ('name', name)
]
print("Building assessor properties:")
print("\n".join("\t{}={}".format(name, value) for name, value in assessorElements))

assessorTitleAttributesDict = {
    'ID': assessor_id,
    'label': assessor_label,
    'project': project,
    ns('xsi','schemaLocation'): schema_location
}

print("Constructing assessor XML\n\tID={}\n\tlabel={}\n\tproject={}".format(assessor_id, assessor_label, project))
E = ElementMaker(namespace=nsdict['icr'], nsmap=nsdict)
assessorXML = E('RoiCollection', assessorTitleAttributesDict,
    E(ns('xnat', 'date'), dt.date.today().isoformat()),
    E(ns('xnat', 'imageSession_ID'), session_id),
    E('UID', uid),
    E('collectionType', 'RTSTRUCT'),
    E('subjectID', subject_id),
    E('references', *[E('seriesUID', seriesUid) for seriesUid in referencedStudyUids]),
    E('name', name)
)

print('Writing assessor XML to {}'.format(assessor_xml_path))
with open(assessor_xml_path, 'wb') as f:
    f.write(xmltostring(assessorXML, pretty_print=True, encoding='UTF-8', xml_declaration=True))
