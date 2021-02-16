import argparse
import os, re
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
        raise Exception("ERROR: create=False and no existing subject with label {}".format(label))
    return xobject


def populateVariables(xobject, row):
    print("Populating custom variables for subject {}".format(xobject.label))
    params = {}
    for key in row.keys():
        if not pd.isna(row[key]):
            #xobject.fields[key.lower()] = row[key]
            var = "xnat:subjectData/fields/field[name={}]/field".format(removeSpecialChars(key.lower()))
            params[var] = row[key]
    r = connection.put(xobject.uri, data = params)
    r.raise_for_status()


def readIntoDataframe(spreadsheet):
    if spreadsheet.endswith('.csv'):
        df = pd.DataFrame(pd.read_csv(spreadsheet))
    else:
        df = pd.DataFrame(pd.read_excel(spreadsheet))
    return df


def removeSpecialChars(string):
    return re.sub("[^0-9a-zA-Z_]+", "", string)


df = readIntoDataframe(args.spreadsheet)
if not args.labelColumn in df.columns:
    printErr("ERROR: no column header matching \"{}\", which you specified as the identifier. Columns are {}".format(args.labelColumn, list(df.columns)))
    exit(1)

errors = False
try:
    connection = xnat.connect(os.environ['XNAT_HOST'], user=os.environ['XNAT_USER'], password=os.environ['XNAT_PASS'])
    project = connection.projects[args.project]
    for index, row in df.iterrows():
        try:
            xobject = getOrCreate(removeSpecialChars(str(row[args.labelColumn])))
            populateVariables(xobject, row)
        except Exception as e:
            printErr(str(e))
            errors = True
finally:
    connection.disconnect()
    
if errors:
    print("Errors encountered during processing, please review the stderr log")
    exit(1)
