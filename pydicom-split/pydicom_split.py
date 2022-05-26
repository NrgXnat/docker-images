#! /usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import math
import os
import sys
import uuid
import warnings
import re
import logging

import numpy

import pydicom
from pydicom.sequence import Sequence
from pydicom.dataset import Dataset

logging.basicConfig(stream=sys.stdout,
                    filemode="w",
                    format="%(levelname)s %(asctime)s - %(message)s",
                    level=logging.DEBUG)

logger = logging.getLogger()

class DICOMDirectory:
    def __init__(self, directory=None):
        logger.debug(f'DICOMDirectory: {directory}')
        self._directory = directory

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, directory):
        self._directory = directory

    def __iter__(self):
        if self._directory is None:
            self.filenames = []
        else:
            self.filenames = os.listdir(self._directory)
        return self

    def __next__(self):
        while self.filenames:
            filename = self.filenames.pop(0)
            path = os.path.join(self._directory, filename)
            if filename.endswith('catalog.xml'):
                logger.info(f'Skipping catalog file: {path}')
                continue
            if filename.endswith('_qc.gif.xml'):
                logger.info(f'Skipping quality control image file: {path}')
                continue
            try:
                logger.debug(f'pydicom.dcmread({path})')
                dataset = pydicom.dcmread(path)
            except pydicom.errors.InvalidDicomError:
                warnings.warn('%s is not a valid DICOM file' % filename)
                continue
            if not hasattr(dataset, 'SOPInstanceUID'):
                warnings.warn('%s is not a valid DICOM file' % filename)
                continue
            return path, dataset
        raise StopIteration

class DICOMSplitterTB:
    def __init__(self, pixel_array=None, axis=0, nT=2, nB=2, offset=5):
        self._pixel_array = pixel_array
        self._axis = axis
        self._nT = nT
        self._nB = nB
        self._offset = offset
        self._nTotal = nB + nT

    @property
    def pixel_array(self):
        return self._pixel_array

    @pixel_array.setter
    def pixel_array(self, pixel_array):
        self._pixel_array = pixel_array

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, axis):
        self._axis = axis

    @property
    def nT(self):
        return self._nT

    @nT.setter
    def nT(self, nT):
        self._nT = nT

    @property
    def nB(self):
        return self._nB

    @nB.setter
    def nB(self, nB):
        self._nB = nB

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset

    def __iter__(self):
        self.index = 0
        if self._pixel_array is not None:
            # assume only 2 row for now
            sizeC = self._pixel_array.shape[1]
            sizeR = self._pixel_array.shape[0]
            self._offsetInPx = math.floor(self._offset / 100 * sizeR)
            self.sizeTC = int(math.floor(sizeC/self._nT))
            self.sizeBC = int(math.floor(sizeC/self._nB))
            self.sizeR = int(math.floor(sizeR/2)) - self._offsetInPx
        return self

    def __next__(self):
        if self.index == self._nTotal:
            raise StopIteration
        index = self.index

        if self._pixel_array is None:
            self.index += 1
            return index, None, None

        start = numpy.zeros(self._pixel_array.ndim, numpy.int16)
        # 1 is column 0 is row
        # at top bed
        if int(math.floor(self.index / self._nT)) == 0:
            # pass
            # print('iterate on top bed')
            remainderC = self._pixel_array.shape[1] % self._nT
            offsetC = max(0, index + 1 + remainderC - self._nT)
            remainderR = self._pixel_array.shape[0] % 2
            offsetR = max(0, index + 1 + remainderR - 2)
            if offsetC:
                warnings.warn('image axis %d not divisible by %d'
                              ', split %d offset 1 pixel from previous split'
                              % (self._axis, self._n, index + 1))
            start[1] = index % self._nT * self.sizeTC + offsetC
            stop = numpy.zeros(self._pixel_array.ndim, numpy.int16)
            stop[1] = start[1] + self.sizeTC

            start[0] = int(math.floor(self.index / self._nT)) * self.sizeR + offsetR
            stop[0] = start[0] + self.sizeR
            indicesC = numpy.arange(start[1], stop[1])
            indicesR = numpy.arange(start[0], stop[0])
        else:
            # print('iterate on bottom bed')
            remainderC = self._pixel_array.shape[1] % self._nB
            offsetC = max(0, (index - self._nT) + 1 + remainderC - self._nB)
            remainderR = self._pixel_array.shape[0] % 2
            offsetR = max(0, (index - self._nT) + 1 + remainderR - 2)
            if offsetC:
                warnings.warn('image axis %d not divisible by %d'
                              ', split %d offset 1 pixel from previous split'
                              % (self._axis, self._nB, index + 1))
            start[1] = (index - self._nT) % self._nB * self.sizeBC + offsetC
            stop = numpy.zeros(self._pixel_array.ndim, numpy.int16)
            stop[1] = start[1] + self.sizeBC

            # assume only 2 row for now
            start[0] = self.sizeR + offsetR
            stop[0] = start[0] + self.sizeR + 2 * self._offsetInPx
            indicesC = numpy.arange(start[1], stop[1])
            indicesR = numpy.arange(start[0], stop[0])
        self.index += 1
        # print ('start and stop')
        # print (start,stop)
        # print (start[0],start[0]+len(indicesR))
        # print (start[1],start[1]+len(indicesC))
        return index, start, self._pixel_array[start[0]:stop[0],start[1]:stop[1]]

class DICOMSplitter:
    def __init__(self, pixel_array=None, axis=0, n=2):
        self._pixel_array = pixel_array
        self._axis = axis
        self._n = n

    @property
    def pixel_array(self):
        return self._pixel_array

    @pixel_array.setter
    def pixel_array(self, pixel_array):
        self._pixel_array = pixel_array

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, axis):
        self._axis = axis

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, n):
        self._n = n

    def __iter__(self):
        self.index = 0
        if self._pixel_array is not None:
            size = self._pixel_array.shape[self._axis]
            self.size = int(math.floor(size/self._n))
        return self

    def __next__(self):
        if self.index == self._n:
            raise StopIteration

        index = self.index

        if self._pixel_array is None:
            self.index += 1
            return index, None, None

        start = numpy.zeros(self._pixel_array.ndim, numpy.int16)
        remainder = self._pixel_array.shape[self._axis] % self._n
        offset = max(0, index + 1 + remainder - self._n)
        if offset:
            warnings.warn('image axis %d not divisible by %d'
                          ', split %d offset 1 pixel from previous split'
                          % (self._axis, self._n, index + 1))
        start[self._axis] = index * self.size + offset
        stop = numpy.zeros(self._pixel_array.ndim, numpy.int16)
        stop[self._axis] = start[self._axis] + self.size
        indices = numpy.arange(start[self._axis], stop[self._axis])
        self.index += 1
        # print(self.index)
        # print(start)
        # print(indices)
        # print(numpy.take(self._pixel_array, indices, self._axis).shape)
        return index, start, numpy.take(self._pixel_array, indices, self._axis)


def x667_uuid():
    return '2.25.%d' % uuid.uuid4()


def parse_patient(patient, delimiter='_'):
    root, *ids = str(patient).split(delimiter)
    trailing = ''
    if ids[-1] in map(str, range(1, 10)):
        warnings.warn('patient %s ends with %s, removing...' % (patient,
                                                                ids[-1]))
        trailing = delimiter + ids.pop()
    return [delimiter.join((root, re.sub("[^0-9]", "", id_))) for id_ in ids], trailing

def parse_patient_TB(patient, delimiter='_'):
    root, *ids = str(patient).split(delimiter)
    tmp = 3 * ['blank']
    trailing = ''
    if ids[-1] in map(str, range(1, 10)):
        warnings.warn('patient %s ends with %s, removing...' % (patient,
                                                                ids[-1]))
        trailing = delimiter + ids.pop()
    # Need to tell the position T, Rp, L
    for id_ in ids:
        if re.search('\(T\)', id_):
            tmp[0] = delimiter.join((root, id_))
        elif re.search('\(L\)', id_):
            tmp[1] = delimiter.join((root, id_))
        elif re.search('\(Rp\)', id_):
            tmp[2] = delimiter.join((root, id_))
    return tmp, trailing


def affine(dataset):
    S = numpy.array(dataset.ImagePositionPatient, numpy.float64)
    F = numpy.array([dataset.ImageOrientationPatient[3:],
                     dataset.ImageOrientationPatient[:3]], numpy.float64).T
    delta_r, delta_c = map(float, dataset.PixelSpacing)
    return numpy.array([[F[0, 0]*delta_r, F[0, 1]*delta_c, 0, S[0]],
                        [F[1, 0]*delta_r, F[1, 1]*delta_c, 0, S[1]],
                        [F[2, 0]*delta_r, F[2, 1]*delta_c, 0, S[2]],
                        [0, 0, 0, 1]])


def directory_name(directory, i):
    return os.path.join(directory.rstrip(os.sep), i)


def make_output_paths(directory, n, output_paths=None):
    if output_paths is None:
        output_paths = [directory_name(directory, i) for i in range(n)]
    for output_path in output_paths:
        try:
            os.mkdir(output_path)
        except FileExistsError:
            pass
    return output_paths


def make_output_path(directory, i, output_path=None):
    if output_path is None:
        output_path = directory_name(directory, i)
    try:
        os.mkdir(output_path)
    except FileExistsError:
        pass
    return output_path


def derive_image_sequence(sop_class_uid, sop_instance_uid):
    source_image = Dataset()
    source_image.ReferencedSOPClassUID = sop_class_uid
    source_image.ReferencedSOPInstanceUID = sop_instance_uid

    purpose_of_reference = Dataset()
    purpose_of_reference.CodeValue = '113130'
    purpose_of_reference.CodingSchemeDesignator = 'DCM'
    purpose_of_reference.CodeMeaning = \
            'Predecessor containing group of imaging subjects'
    source_image.PurposeOfReferenceCodeSequence = \
            Sequence([purpose_of_reference])
    derivation_image = Dataset()
    derivation_image.SourceImageSequence = Sequence([source_image])
    derivation_code = Dataset()
    derivation_code.CodeValue = '113131'
    derivation_code.CodingSchemeDesignator = 'DCM'
    derivation_code.CodeMeaning = \
            'Extraction of individual subject from group'
    derivation_image.DerivationCodeSequence = Sequence([derivation_code])
    derivation_image_sequence = Sequence([derivation_image])

    return derivation_image_sequence
def get_patient_TB(patient_name, patient_id, n, patient_names=None, patient_ids=None, order=None):
    name_trailing, id_trailing = '', ''
    if patient_names is None:
        patient_names, name_trailing = parse_patient_TB(patient_name)
    if patient_ids is None:
        patient_ids, id_trailing = parse_patient_TB(patient_name)
        # in case patient id format is different
        # patient_ids, id_trailing = parse_patient(patient_id)
    # print(patient_names)
    if len(patient_names) != n:
        tmpName = 3 * ['blank']
        for i in range(len(order)):
            if int(order[i]) != 0:
                try:
                    tmpName[i] = patient_names.pop(0)
                except:
                    continue
        patient_names = tmpName
        warnings.warn('failed to parse PatientName %s, append a blank' % patient_name)
    if len(patient_ids) != n:
        tmpId = 3 * ['blank']
        for i in range(len(order)):
            if int(order[i]) != 0:
                try:
                    tmpId[i] = patient_ids.pop(0)
                except:
                    continue
        patient_ids = tmpId
        warnings.warn('failed to parse PatientID %s, append a blank' % patient_id)
    source_patient = Dataset()
    # FIXME: remove '_1'?
    source_patient.PatientName = patient_name
    source_patient.PatientID = patient_id

    return (patient_names, patient_ids), Sequence([source_patient]), (name_trailing, id_trailing)
def get_patient(patient_name, patient_id, n, patient_names=None, patient_ids=None, order=None):
    name_trailing, id_trailing = '', ''
    if patient_names is None:
        patient_names, name_trailing = parse_patient(patient_name)
    if patient_ids is None:
        patient_ids, id_trailing = parse_patient(patient_name)
        # in case patient id format is different
        # patient_ids, id_trailing = parse_patient(patient_id)
    # print(patient_names)
    if len(patient_names) != n:
        tmpName = 3 * ['blank']
        for i in range(len(order)):
            if int(order[i]) != 0:
                try:
                    tmpName[i] = patient_names.pop(0)
                except:
                    continue
        patient_names = tmpName
        warnings.warn('failed to parse PatientName %s, append a blank' % patient_name)
    if len(patient_ids) != n:
        tmpId = 3 * ['blank']
        for i in range(len(order)):
            if int(order[i]) != 0:
                try:
                    tmpId[i] = patient_ids.pop(0)
                except:
                    continue
        patient_ids = tmpId
        warnings.warn('failed to parse PatientID %s, append a blank' % patient_id)
    source_patient = Dataset()
    # FIXME: remove '_1'?
    source_patient.PatientName = patient_name
    source_patient.PatientID = patient_id

    return (patient_names, patient_ids), Sequence([source_patient]), (name_trailing, id_trailing)


def set_pixel_data(dataset, pixel_array):
    dataset.PixelData = pixel_array.tostring()
    dataset.Rows, dataset.Columns = pixel_array.shape

def checkDirectory(directory, output_dir=None):
    logger.debug(f'checkDirectory({directory}, {output_dir})')
    for root, subdirs, files in os.walk(directory):
        if len(files):
            if files.pop(0) != '.DS_Store':
                newRoot = output_dir
                for subdirs in [os.path.basename(directory), *os.path.relpath(root, directory).split('/')]:
                    newRoot = os.path.join(newRoot, subdirs)
                if not os.path.exists(newRoot):
                    os.makedirs(newRoot, exist_ok=True)
                logger.debug(f'checkDirectory yield root: {root} newRoot: {newRoot}')
                yield root, newRoot
def split_dicom_directory(directory, axis=0, n=3, nTB=None, offset=5, keep_origin=False,
                          study_instance_uids=None, series_instance_uids=None,
                          series_descriptions=None, output_dir=None,
                          derivation_description=None, patient_names=None,
                          patient_ids=None, order=None, orderT=None, orderB=None,
                          patient_weights=None, patient_orientations=None, patient_comments=None,
                          ra_ph_start_times=None, ra_nuc_tot_doses=None):
    logger.info(f'Splitting directory {directory}')
    if nTB is not None:
        orderT = orderT.split(',')
        orderB = orderB.split(',')
        if int(nTB.split(',')[0]) != len(orderT):
            raise Exception('[ERROR] # of split has to equal to length of order on Top')
        if int(nTB.split(',')[1]) != len(orderB):
            raise Exception('[ERROR] # of split has to equal to length of order on Bottom')
        order = orderT + orderB
        nT = int(nTB.split(',')[0])
        nB = int(nTB.split(',')[1])
        n = nT + nB
    else:
        order = order.split(',')
        if n != len(order):
            raise Exception('[ERROR] # of split has to equal to length of order')
        if series_instance_uids:
            n = len(series_instance_uids)
        if n is None:
            raise ValueError
        if series_descriptions and len(series_descriptions) != n:
            raise ValueError
        if study_instance_uids and len(study_instance_uids) != n:
            raise ValueError

    if patient_weights and n != len(patient_weights):
        raise Exception('[ERROR] # of patient_weights has to equal to n')

    if patient_orientations and n != len(patient_orientations):
        raise Exception('[ERROR] # of patient_orientation has to equal to n')

    if patient_comments and n != len(patient_comments):
        raise Exception('[ERROR] # of patient_comments has to equal to n')

    if ra_ph_start_times and n != len(ra_ph_start_times):
        raise Exception('[ERROR] # of ra_ph_start_times has to equal to n')

    if ra_nuc_tot_doses and n != len(ra_nuc_tot_doses):
        raise Exception('[ERROR] # of ra_nuc_tot_dose has to equal to n')

    outputs = {}  # PatientName -> [split dcm files]

    for directoryChecked, newRoot in checkDirectory(directory, output_dir):

        series_instance_uids = [x667_uuid() for i in range(n)]

        for path, dataset in DICOMDirectory(directoryChecked):
            try:
                pixel_array = dataset.pixel_array
            except (TypeError, AttributeError):
                pixel_array = None
            if nTB is not None:
                nT = int(nTB.split(',')[0])
                nB = int(nTB.split(',')[1])
                dicom_splitter = DICOMSplitterTB(pixel_array, axis, nT, nB, offset)
                n = nT + nB
            else:
                dicom_splitter = DICOMSplitter(pixel_array, axis, n)
            dataset.ImageType = ['DERIVED', 'PRIMARY', 'SPLIT']

            dataset.DerivationDescription = derivation_description

            dataset.DerivationImageSequence = derive_image_sequence(dataset.SOPClassUID, dataset.SOPInstanceUID)
            if nTB is not None:
                parsed, dataset.SourcePatientGroupIdentificationSequence, trailing = get_patient_TB(dataset.PatientName,
                                                                                                 dataset.PatientID, n,
                                                                                                 patient_names,
                                                                                                 patient_ids, order)
            else:
                parsed, dataset.SourcePatientGroupIdentificationSequence, trailing = get_patient(dataset.PatientName, dataset.PatientID, n, patient_names, patient_ids, order)


            parsed_patient_names, parsed_patient_ids = parsed

            for name in parsed_patient_names:
                if name not in outputs:
                    outputs[name] = []

            name_trailing, id_trailing = trailing

            if not study_instance_uids:
                study_instance_uids = [x667_uuid() for i in range(n)]

            for i, origin, pixel_array in dicom_splitter:
                if parsed_patient_names[i] != 'blank':
                    split_dataset = copy.deepcopy(dataset)

                    if pixel_array is not None:
                        set_pixel_data(split_dataset, pixel_array)

                        if not keep_origin:
                            affine_matrix = affine(dataset)
                            position = affine_matrix.dot(numpy.append(origin, [0, 1]))
                            # maximum 16 characters
                            split_dataset.ImagePositionPatient = [str(p)[:16] for p in position[:3]]

                    split_dataset.SOPInstanceUID = x667_uuid()
                    split_dataset.file_meta.MediaStorageSOPInstanceUID = split_dataset.SOPInstanceUID

                    split_dataset.StudyInstanceUID = study_instance_uids[i]

                    split_dataset.SeriesInstanceUID = series_instance_uids[i]
                    split_dataset.StorageMediaFileSetUID = series_instance_uids[i] + '.0'

                    if series_descriptions:
                        split_dataset.SeriesDescription = series_descriptions[i]
                    else:
                        if 'SeriesDescription' in split_dataset:
                            split_dataset.SeriesDescription += ' split ' + parsed_patient_ids[i]
                        else:
                            split_dataset.SeriesDescription = 'split ' + parsed_patient_ids[i]

                    split_dataset.PatientName = parsed_patient_names[i]
                    split_dataset.PatientID = parsed_patient_ids[i]

                    if patient_weights:
                        split_dataset.PatientWeight = patient_weights[i]

                    if patient_comments:
                        split_dataset.PatientComments = patient_comments[i]

                    if patient_orientations:
                        split_dataset.PatientOrientation = patient_orientations[i]

                    if split_dataset.Modality == 'PT':
                        if ra_ph_start_times:
                            split_dataset.RadiopharmaceuticalInformationSequence[0].RadiopharmaceuticalStartTime = \
                                ra_ph_start_times[i]
                        if ra_nuc_tot_doses:
                            split_dataset.RadiopharmaceuticalInformationSequence[0].RadionuclideTotalDose = \
                                ra_nuc_tot_doses[i]

                    created_output_path = make_output_path(newRoot, parsed_patient_names[i], None)
                    filename = os.path.join(created_output_path, os.path.basename(path))
                    split_dataset.save_as(filename)
                    outputs[parsed_patient_names[i]].append(filename)

    return outputs


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('DICOM_DIRECTORY', nargs='*')
    parser.add_argument('-a', '--axis', type=int, default=1,
                        help='axis (0 for rows, 1 for columns)'
                             ', default columns')
    parser.add_argument('-o', '--keep_origin', action='store_true',
                        help='origin position from offset from original'
                             ' volume, default no')
    parser.add_argument('-s', '--study_instance_uids', nargs='*',
                        help='set the study instance UIDs')
    parser.add_argument('-S', '--unique_study_instance_uids',
                        action='store_true',
                        help='shared the study instance UID in all series')
    parser.add_argument('-d', '--series_descriptions', nargs='*',
                        help='set the series descriptions')
    parser.add_argument('-v', '--derivation_description',
                        default='Original volume split into equal subvolumes for each patient',
                        help='set the derivation description')
    parser.add_argument('-p', '--patient_names', nargs='*',
                        help='patient names')
    parser.add_argument('-i', '--patient_ids', nargs='*', help='patient ids')
    parser.add_argument('-O', '--output_paths', nargs='*', help='output path names')
    parser.add_argument('-Outdir', '--output_dir', help='save in new output directory')
    parser.add_argument('-X', '--mangle_output_paths', action='store_true',
                        help='set output path to split patient ID plus'
                             'trailing characters')

    parser.add_argument('-order', '--order', help='order of patient placed in scanner', default='1,1,1')
    parser.add_argument('-orderT', '--orderT', help='order of patient placed in scanner of top bed', default='1,1,1')
    parser.add_argument('-orderB', '--orderB', help='order of patient placed in scanner of bottom bed', default='1,1,1')
    parser.add_argument('-offset', '--offset', type=int, default=5,
                        help='offset from center, default 5 percent from center')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-n', type=int, help='split into N volumes')
    group.add_argument('-nTB', nargs='*', help='split into N volumes of top and bottom beds')

    group.add_argument('-u', '--series_instance_uids', nargs='*', default=[],
                       help='split volume for each series instance UID')

    kwargs = vars(parser.parse_args())

    directories = kwargs.pop('DICOM_DIRECTORY')

    shared = not kwargs.pop('unique_study_instance_uids')
    if shared and not kwargs.get('study_instance_uids'):
        if kwargs.get('nTB') is not None:
            n = int(kwargs.get('nTB')[0].split(',')[0]) + int(kwargs.get('nTB')[0].split(',')[1])
            n = len(kwargs.get('series_instance_uids')) or n
        else:
            n = len(kwargs.get('series_instance_uids')) or kwargs.get('n')
        kwargs['study_instance_uids'] = [x667_uuid() for i in range(n)]

    for directory in directories:
        split_dicom_directory(directory, **kwargs)
