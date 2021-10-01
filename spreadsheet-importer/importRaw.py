import csv, os
import argparse
import pandas as pd

from sys import stderr
from xnatjsession import XnatSession

parser = argparse.ArgumentParser(description="Run spreadsheet importer")
parser.add_argument("--project", help="Project", required=True)
parser.add_argument("--spreadsheet", help="Spreadsheet to import (csv or Excel)", required=True)
parser.add_argument("--labelColumn", help="Column that identifies the object in XNAT", required=False, default="")
parser.add_argument("--create", action="store_true", help="Create XNAT object if it does not exist", required=False)
#TODO add support for other datatypes
#parser.add_argument("--datatype", help="Type of XNAT object (Subject or Experiment)", required=False, default="Experiment")

args = parser.parse_args()

def printErr(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


def makeUrlParams(row):
    params = {}
    for key in row.keys():
        if row[key] and not pd.isna(row[key]):
            var = "xnat:subjectData/fields/field[name={}]/field".format(key.lower())
            params[var] = row[key]
    return params


def doesSubjectExist(url):
    session.renew_httpsession()
    return session.httpsess.get(url).status_code == 200


def createSubject(subject, url):
    session.renew_httpsession()
    print("|> Creating subject: {}".format(subject))
    r = session.httpsess.put(url)
    r.raise_for_status()
    print("|> Success.")


def populateVariables(subject, url, params):
    session.renew_httpsession()
    print("|> Populating variables for subject: {}".format(subject))
    r = session.httpsess.put(url, params = params)
    r.raise_for_status()
    print("|> Success.")


def readIntoDataframe(spreadsheet):
    if spreadsheet.endswith('.csv'):
        df = pd.DataFrame(pd.read_csv(spreadsheet))
    else:
        df = pd.DataFrame(pd.read_excel(spreadsheet))
    return df


try:
    ERRORS_FOUND = False
    session = XnatSession(username=os.environ['XNAT_USER'], password=os.environ['XNAT_PASS'], host=os.environ['XNAT_HOST'])
    projectUrl = "{}/data/projects/{}".format(os.environ['XNAT_HOST'], PROJECT)
    df = readIntoDataframe(args.spreadsheet)
    for index, row in df.iterrows():
        try:
            subject = str(row[args.labelColumn])
            subjectUrl = "{}/subjects/{}".format(projectUrl, subject)
            if not doesSubjectExist(subjectUrl):
                if args.create:
                    createSubject(subject, subjectUrl)
                else:
                    raise Exception("|> ERROR: no subject with label {} and create=False".format(subject))
            populateVariables(subject, subjectUrl, makeUrlParams(row))
        except Exception as e:
            printErr("|> ERROR subject {}: {}".format(subject, str(e)))
            ERRORS_FOUND = True

    if ERRORS_FOUND:
        raise Exception("Errors encountered during processing, please review the stderr log")


finally:
    session.close_httpsession()
