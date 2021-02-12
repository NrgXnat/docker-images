import argparse
import os
import xnat
import pandas as pd
from sys import stderr

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


def getOrCreate(label):
    objects = project.subjects
    if label in objects:
        xobject = objects[label]
    elif args.create:
        print("Creating subject {}".format(label))
        xobject = connection.classes.SubjectData(parent=project, label=label)
    else:
        raise Exception("ERROR: no subject with label {} and create=False".format(label))
    return xobject


def populateVariables(xobject, row):
    print("Populating custom variables for subject {}".format(xobject.label))
    params = {}
    for key in row.keys():
        if row[key] and not pd.isna(row[key]):
            #xobject.fields[key.lower()] = row[key]
            var = "xnat:subjectData/fields/field[name={}]/field".format(key.lower())
            params[var] = row[key]
    connection.put(xobject.uri, data = params)


def readIntoDataframe(spreadsheet):
    if spreadsheet.endswith('.csv'):
        df = pd.DataFrame(pd.read_csv(spreadsheet))
    else:
        df = pd.DataFrame(pd.read_excel(spreadsheet))
    return df


try:
    errors = False
    connection = xnat.connect(os.environ['XNAT_HOST'], user=os.environ['XNAT_USER'], password=os.environ['XNAT_PASS'])
    project = connection.projects[args.project]
    df = readIntoDataframe(args.spreadsheet)
    for index, row in df.iterrows():
        try:
            xobject = getOrCreate(str(row[args.labelColumn]))
            populateVariables(xobject, row)
        except Exception as e:
            printErr(str(e))
            errors = True

    if errors:
        raise Exception("Errors encountered during processing, please review the stderr log")
        
finally:
    connection.disconnect()
