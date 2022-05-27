import matplotlib.pyplot as plt
import numpy as np
import os
import pydicom_split
import requests
import zipfile
import json
import logging
import sys

from pydicom import dcmread
from requests.auth import HTTPBasicAuth

logging.basicConfig(stream=sys.stdout,
                    filemode="w",
                    format="%(levelname)s %(asctime)s - %(message)s",
                    level=logging.DEBUG)

logger = logging.getLogger()

def run_pydicom_split(username: str, password: str, xnat_host: str, project_id: str, session_label: str, offset: int,
                      input_directory: str, output_directory: str):

    if xnat_host == 'http://localhost':
        xnat_host = 'http://host.docker.internal'

    update_scan_record_status(username, password, xnat_host, project_id, f'{session_label}_scan_record', "Splitting In Progress")

    try:
        logger.info(f'Processing project: {project_id}, session: + {session_label}, directory: {input_directory}')
        logger.debug(xnat_host)

        hotel_scan_record = get_hotel_scan_record(username, password, xnat_host, project_id, session_label)

        num_rows = max([subj['position']['y'] for subj in hotel_scan_record['hotelSubjects']])
        logger.debug("Number of rows: " + str(num_rows))

        if num_rows == 1:
            split_output = run_pydicom_split_one_row(input_directory=input_directory,
                                                     output_directory=output_directory,
                                                     hotel_scan_record=hotel_scan_record,
                                                     offset=offset)
        elif num_rows == 2:
            split_output = run_pydicom_split_two_rows(input_directory=input_directory,
                                                      output_directory=output_directory,
                                                      hotel_scan_record=hotel_scan_record,
                                                      offset=offset)
        else:
            raise Exception('[ERROR] Cannot split more than two rows.')

        for patient_name in split_output.keys():
            if patient_name == '' or patient_name == 'blank':
                continue

            filename = os.path.join(output_directory, patient_name) + '.zip'

            with zipfile.ZipFile(filename, 'w') as zf:
                for dcm_file in split_output[patient_name]:
                    zf.write(dcm_file, os.path.relpath(dcm_file, output_directory))

            logger.info(f'Zip file created for subject {patient_name}')

            send_session_to_xnat(username=username, password=password, xnat_host=xnat_host, project_id=project_id,
                                 subject_label=patient_name, session_label=session_label, dcm_zip=filename)

        update_scan_record(username=username, password=password, xnat_host=xnat_host, session_label=session_label,
                           hotel_scan_record=hotel_scan_record)

        generate_qc_montage(split_output=split_output, output_directory=output_directory)

        update_scan_record_status(username, password, xnat_host, project_id, f'{session_label}_scan_record', "Split Complete")

    except Exception as e:
        logger.exception("Fatal error while splitting hotel scan: " + str(e))
        update_scan_record_status(username, password, xnat_host, project_id, f'{session_label}_scan_record', "Error: Not Split")
        sys.exit("Fatal error while splitting hotel scan " + str(e))


def send_session_to_xnat(username: str, password: str, xnat_host: str, project_id: str, subject_label: str,
                         session_label: str, dcm_zip: zipfile):

    dest_url = f'{xnat_host}/data/services/import'
    parameters = {
        'import-handler': 'DICOM-zip',
        'rename': 'true',
        'overwrite': 'append',
        'PROJECT_ID': project_id,
        'SUBJECT_ID': subject_label,
        'EXPT_LABEL': session_label + "_split_" + subject_label
    }

    logger.info(f'Uploading splitter output for project: {project_id} , session: {session_label} , subject: {subject_label} to {dest_url}')

    r = requests.post(dest_url,
                      auth=HTTPBasicAuth(username, password),
                      params=parameters,
                      files={'file': open(dcm_zip, 'rb')})

    if r.status_code == 200:
        logger.info(f'Splitter output for project: {project_id} , session: {session_label} , subject: {subject_label} successfully uploaded to XNAT')
    elif r.status_code == 504:
        logger.warning(
            f'Splitter output for project: {project_id} , session: {session_label} , subject: {subject_label} uploaded to'
            f' XNAT with unknown success. Server response 504 usually indicates a long upload not a failure.')
    else:
        raise Exception(f'Failed to upload splitter output for project: {project_id} , session: {session_label} , subject:'
                        f' {subject_label}')


def update_scan_record(username: str, password: str, xnat_host: str, session_label: str, hotel_scan_record: dict):

    project_id = hotel_scan_record['projectID']

    subjects = {}

    for subject in hotel_scan_record['hotelSubjects']:
        subject_id = subject['subjectId'] if 'subjectId' in subject else ''
        subject_label = subject['subjectLabel'] if 'subjectLabel' in subject else ''

        if subject_id and subject_label:
            subjects[subject_id] = f"{session_label}_split_{subject_label}"

    url = f"{xnat_host}/xapi/pixi/hotelscanrecords/{session_label}_scan_record/project/{project_id}/subjects"

    logger.info(f'Updating scan record at {url}')

    r = requests.put(url,
                     auth=HTTPBasicAuth(username, password),
                     headers={'Content-type': 'application/json'},
                     data=json.dumps(subjects))
    if r.ok:
        logger.info('Hotel scan record updated')
    else:
        logger.error("Failed to update hotel scan record")

def update_scan_record_status(username: str, password: str, xnat_host: str, project_id: str, scan_record_label: str,
                              status: str):
    url = f"{xnat_host}/xapi/pixi/hotelscanrecords/{scan_record_label}/project/{project_id}/status"

    logger.debug(f'Updating scan record status: {scan_record_label} // {status}')

    r = requests.put(url,
                     auth=HTTPBasicAuth(username, password),
                     headers={'Content-type': 'text/plain'},
                     data=status)

    if r.ok:
        logger.debug('Hotel scan record status updated.')
    else:
        logger.error("Failed to update hotel scan record.")


def generate_qc_montage(split_output: dict, output_directory: str):

    for patient_name in split_output.keys():
        if patient_name == '' or patient_name == 'blank':
            continue

        logger.info(f"Generating QC Snapshot for subject: {patient_name}")

        dicom_files = split_output[patient_name]
        num_files = len(dicom_files)

        fig = plt.figure(figsize=(10, 5))
        fig.suptitle(f'Subject: {patient_name}')
        rows = 3
        columns = 3

        # Sample the files evenly spaced
        idx_files = np.unique(np.round(np.linspace(0, num_files - 1, 9))).astype(int)

        for iSubplot in range(len(idx_files) if len(idx_files) < 9 else 9):
            ds = dcmread(dicom_files[idx_files[iSubplot]])
            fig.add_subplot(rows, columns, iSubplot + 1)
            plt.imshow(ds.pixel_array, cmap=plt.cm.gray)
            plt.axis('off')

        qc_output_path = os.path.join(output_directory, 'qc-snapshots')
        if not os.path.exists(qc_output_path):
            os.mkdir(qc_output_path)

        plt.savefig(os.path.join(qc_output_path, f'{patient_name}-qc-snapshot.png'))
        logger.info(f"Saved QC Snapshot for subject: {patient_name}")


def get_hotel_scan_record(username, password, host, project_id, session_label):
    url = f"{host}/xapi/pixi/hotelscanrecords/{session_label}_scan_record/project/{project_id}"

    logger.info("Retrieving hotel scan record from " + url)

    r = requests.get(url, auth=HTTPBasicAuth(username, password))

    if r.status_code == 200:
        logger.info("Hotel scan record successfully retrieved")
        return r.json()
    else:
        logger.error("Unable to fetch Hotel Scan Record from XNAT")
        raise Exception("Unable to fetch Hotel Scan Record from XNAT")


def run_pydicom_split_one_row(input_directory: str, output_directory: str, hotel_scan_record: dict, offset: int) -> dict:
    n = len(hotel_scan_record['hotelSubjects'])
    patient_names = ['blank'] * n
    order = ['0'] * n
    patient_weights = [0] * n
    patient_orientations = [''] * n
    patient_comments = [''] * n
    ra_ph_start_times = [''] * n
    ra_nuc_tot_doses = [0] * n

    for subject in hotel_scan_record['hotelSubjects']:
        index = subject['position']['x'] - 1
        patient_names[index] = subject['subjectLabel'] if 'subjectLabel' in subject else 'blank'
        patient_weights[index] = subject['weight'] * pow(10, -3) if 'weight' in subject else 0
        patient_orientations[index] = subject['orientation'] if 'orientation' in subject else ''
        patient_comments[index] = subject['notes'] if 'notes' in subject else ''
        ra_ph_start_times[index] = subject['injectionTime'] if 'injectionTime' in subject else ''
        ra_nuc_tot_doses[index] = subject['activity'] * 37 * pow(10, 6) if 'activity' in subject else 0

        if patient_names[index] == '' or patient_names[index] == 'blank':
            patient_names[index] = 'blank'
            order[index] = '0'
        else:
            order[index] = '1'

    order = ','.join(order)

    logger.info("Running pydicom split...")
    split_output = pydicom_split.split_dicom_directory(directory=input_directory,
                                                       axis=1,
                                                       n=n,
                                                       patient_names=patient_names,
                                                       patient_ids=patient_names,
                                                       order=order,
                                                       output_dir=output_directory,
                                                       patient_weights=patient_weights,
                                                       patient_orientations=patient_orientations,
                                                       patient_comments=patient_comments,
                                                       ra_ph_start_times=ra_ph_start_times,
                                                       ra_nuc_tot_doses=ra_nuc_tot_doses,
                                                       offset=offset)
    logger.info("Session/directory split successfully")
    return split_output


def run_pydicom_split_two_rows(input_directory: str, output_directory: str, hotel_scan_record: dict,
                               offset: int) -> dict:
    top_row_subjects = list(filter(lambda subj: subj['position']['y'] == 1, hotel_scan_record['hotelSubjects']))
    bottom_row_subjects = list(filter(lambda subj: subj['position']['y'] == 2, hotel_scan_record['hotelSubjects']))

    n = len(hotel_scan_record['hotelSubjects'])
    n_t = len(top_row_subjects)
    n_b = len(bottom_row_subjects)

    assert n_t + n_b == n

    patient_names = ['blank'] * n
    orderT = ['0'] * n_t
    orderB = ['0'] * n_b
    patient_weights = [0] * n
    patient_orientations = [''] * n
    patient_comments = [''] * n
    ra_ph_start_times = [''] * n
    ra_nuc_tot_doses = [0] * n

    for subject in top_row_subjects:
        index = subject['position']['x'] - 1
        patient_names[index] = subject['subjectLabel'] if 'subjectLabel' in subject else 'blank'
        patient_weights[index] = subject['weight'] * pow(10, -3) if 'weight' in subject else 0
        patient_orientations[index] = subject['orientation'] if 'orientation' in subject else ''
        patient_comments[index] = subject['notes'] if 'notes' in subject else ''
        ra_ph_start_times[index] = subject['injectionTime'] if 'injectionTime' in subject else ''
        ra_nuc_tot_doses[index] = subject['activity'] * 37 * pow(10, 6) if 'activity' in subject else 0

        if patient_names[index] == '' or patient_names[index] == 'blank':
            patient_names[index] = 'blank'
            orderT[index] = '0'
        else:
            orderT[index] = '1'

    for subject in bottom_row_subjects:
        index = subject['position']['x'] - 1 + n_t
        index_b = subject['position']['x'] - 1
        patient_names[index] = subject['subjectLabel'] if 'subjectLabel' in subject else 'blank'
        patient_weights[index] = subject['weight'] * pow(10, -3) if 'weight' in subject else 0
        patient_orientations[index] = subject['orientation'] if 'orientation' in subject else ''
        patient_comments[index] = subject['notes'] if 'notes' in subject else ''
        ra_ph_start_times[index] = subject['injectionTime'] if 'injectionTime' in subject else ''
        ra_nuc_tot_doses[index] = subject['activity'] * 37 * pow(10, 6) if 'activity' in subject else 0

        if patient_names[index] == '' or patient_names[index] == 'blank':
            patient_names[index] = 'blank'
            orderB[index_b] = '0'
        else:
            orderB[index_b] = '1'

    n_tb = '{n_t},{n_b}'.format(n_t=n_t, n_b=n_b)
    orderT = ','.join(orderT)
    orderB = ','.join(orderB)

    # axis?
    logger.info("Running pydicom split...")
    split_output = pydicom_split.split_dicom_directory(directory=input_directory,
                                                       axis=1,
                                                       nTB=n_tb,
                                                       patient_names=patient_names,
                                                       patient_ids=patient_names,
                                                       orderT=orderT,
                                                       orderB=orderB,
                                                       output_dir=output_directory,
                                                       patient_weights=patient_weights,
                                                       patient_orientations=patient_orientations,
                                                       patient_comments=patient_comments,
                                                       ra_ph_start_times=ra_ph_start_times,
                                                       ra_nuc_tot_doses=ra_nuc_tot_doses,
                                                       offset=offset)

    logger.info("Session/directory split successfully")
    return split_output


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('DICOM_DIRECTORY', nargs='*')
    parser.add_argument('-u', '--username', type=str, default=None, required=True, help="XNAT username")
    parser.add_argument('-p', '--password', type=str, default=None, required=True, help="XNAT password")
    parser.add_argument('-s', '--xnat_host', type=str, default=None, required=True, help="XNAT Host")
    parser.add_argument('--project_id', type=str, default=None, required=True, help="XNAT Project ID")
    parser.add_argument('--session_label', type=str, default=None, required=True, help="XNAT Hotel Session Label")
    parser.add_argument('--output_directory', type=str, default=None, required=True, help="Output directory")
    parser.add_argument('-offset', '--offset', type=int, default=5,
                        help='offset from center, default 5 percent from center')

    kwargs = vars(parser.parse_args())
    directories = kwargs.pop('DICOM_DIRECTORY')

    for directory in directories:
        run_pydicom_split(input_directory=directory, **kwargs)
