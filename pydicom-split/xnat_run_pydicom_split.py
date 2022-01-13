import matplotlib.pyplot as plt
import numpy as np
import os
import pydicom_split
import requests
import zipfile

from pydicom import dcmread
from requests.auth import HTTPBasicAuth


def run_pydicom_split(username: str, password: str, xnat_url: str, project_id: str, session_id: str, offset: int,
                      input_directory: str, output_directory: str, hotel_session_label_identifier: str):

    print("Processing project: " + project_id + " , session: " + session_id + " , directory: " + input_directory)

    if xnat_url == 'http://localhost':
        xnat_url = 'http://host.docker.internal'

    hotel_scan_record = get_hotel_scan_record(username, password, xnat_url, project_id, session_id)

    num_rows = max([subj['position']['y'] for subj in hotel_scan_record['hotelSubjects']])
    print("Number of rows: " + str(num_rows))

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

        print(f'Zip file created for subject {patient_name}')

        send_session_to_xnat(username=username, password=password, xnat_url=xnat_url, project_id=project_id,
                             subject_id=patient_name, session_id=session_id, dcm_zip=filename,
                             hotel_session_label_identifier=hotel_session_label_identifier)

    generate_qc_montage(split_output=split_output, output_directory=output_directory)


def send_session_to_xnat(username: str, password: str, xnat_url: str, project_id: str, subject_id: str, session_id: str,
                         dcm_zip: zipfile, hotel_session_label_identifier="Hotel"):

    if session_id.startswith(f'{hotel_session_label_identifier}_'):
        session_id = session_id.replace(f'{hotel_session_label_identifier}_', '')

    dest_url = f'{xnat_url}/data/services/import'
    parameters = {
        'import-handler': 'DICOM-zip',
        'rename': 'true',
        'overwrite': 'append',
        'PROJECT_ID': project_id,
        'SUBJECT_ID': subject_id,
        'EXPT_LABEL': session_id + "_split_" + subject_id
    }

    print(f'Uploading splitter output for project: {project_id} , session: {session_id} , subject: {subject_id} to {dest_url}')

    r = requests.post(dest_url,
                      auth=HTTPBasicAuth(username, password),
                      params=parameters,
                      files={'file': open(dcm_zip, 'rb')})

    if r.status_code == 200:
        print(f'Splitter output for project: {project_id} , session: {session_id} , subject: {subject_id} successfully uploaded to XNAT')
    elif r.status_code == 504:
        print(
            f'Splitter output for project: {project_id} , session: {session_id} , subject: {subject_id} uploaded to'
            f' XNAT with unknown success. Server response 504 usually indicates a long upload not a failure.')
    else:
        raise Exception(f'Failed to upload splitter output for project: {project_id} , session: {session_id} , subject: {subject_id}')

def get_hotel_session_label_identifier(username: str, password: str, xnat_url: str):

    url = f'{xnat_url}/xapi/pixi/preferences/hotelSessionLabelIdentifier'
    r = requests.get(url, auth=HTTPBasicAuth(username, password))

    if r.status_code == 200:
        return r.text
    else:
        return "Hotel"


def generate_qc_montage(split_output: dict, output_directory: str):

    for patient_name in split_output.keys():
        if patient_name == '' or patient_name == 'blank':
            continue

        print(f"Generating QC Snapshot for subject: {patient_name}")

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
        print(f"Saved QC Snapshot for subject: {patient_name}")


def get_hotel_scan_record(username, password, host, projectID, sessionID):
    url = "{host}/xapi/pixi/hotelscanrecords/project/{projectID}/{sessionID}".format(host=host,
                                                                                     projectID=projectID,
                                                                                     sessionID=sessionID)

    print("Retrieving hotel scan record from " + url)

    r = requests.get(url, auth=HTTPBasicAuth(username, password))

    if r.status_code == 200:
        print("Hotel scan record successfully retrieved")
        return r.json()
    else:
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

    print("Running pydicom split...")
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
    print("Session/directory split successfully")
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
    print("Running pydicom split...")
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

    print("Session/directory split successfully")
    return split_output


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('DICOM_DIRECTORY', nargs='*')
    parser.add_argument('-u', '--username', type=str, default=None, required=True, help="XNAT username")
    parser.add_argument('-p', '--password', type=str, default=None, required=True, help="XNAT password")
    parser.add_argument('-s', '--xnat_url', type=str, default=None, required=True, help="XNAT URL")
    parser.add_argument('--project_id', type=str, default=None, required=True, help="XNAT Project ID")
    parser.add_argument('--session_id', type=str, default=None, required=True, help="XNAT Hotel Session ID")
    parser.add_argument('--output_directory', type=str, default=None, required=True, help="Output directory")
    parser.add_argument('--hotel_session_label_identifier', type=str, default="Hotel", required=False,
                        help="Keyword which identifies a hotel vs single subject session. This will be removed from the"
                             " single subject session label.")
    parser.add_argument('-offset', '--offset', type=int, default=5,
                        help='offset from center, default 5 percent from center')

    kwargs = vars(parser.parse_args())
    directories = kwargs.pop('DICOM_DIRECTORY')

    for directory in directories:
        run_pydicom_split(input_directory=directory, **kwargs)
