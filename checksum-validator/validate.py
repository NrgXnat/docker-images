import argparse
import sys
import os
import hashlib
import glob
import re
from xnatjsession import XnatSession

parser = argparse.ArgumentParser(description="Run checksum validation")

parser.add_argument("--sessionId", help="Session ID", required=True)
parser.add_argument("--sessionLabel", help="Session Label", required=True)
parser.add_argument("--project", help="Project", required=True)
parser.add_argument("--subject", help="Subject", required=True)
parser.add_argument("--assignTo", help="Assign query to this user", required=True)
parser.add_argument("--checksumResource", help="Checksum file resource directory", required=False)
parser.add_argument("--checksumSubdir", help="Checksum file subdirectory within checksumResource", required=False, default="")
parser.add_argument("--series", action="append", help="DICOM series XNAT ID", required=False)
parser.add_argument("--dicom", action="store_true", help="Validate DICOM checksum (instead of native zip)", required=False)

args = parser.parse_args()

sesid       = args.sessionId
label       = args.sessionLabel
project     = args.project
subject     = args.subject
assignTo    = args.assignTo
series      = args.series
resdir      = args.checksumResource
subdir      = args.checksumSubdir
dicom       = args.dicom

def create_query(xnatSession, category, title, description):
    uri = "/data/experiments/%s/issues" % sesid
    data = {"status": "OPEN", "categories": category, "title": title, \
        "description": description, "assignedto": assignTo}
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.post(url = xnatSession.host + uri, data = data)
    if response.status_code != 200:
        raise Exception("Error creating query (%s): %s %s %s" % (uri,
                                                                response.status_code,
                                                                response.reason,
                                                                response.text))

def mark_native_files_valid(xnatSession, valid):
    uri = "/data/projects/%s/subjects/%s/experiments/%s" % (project, subject, sesid)
    if valid:
        v = "true"
    else:
        v = "false"
    print("Setting nativeValid to %s" % v)
    uri += "?xnat%3AexperimentData%2Ffields%2Ffield%5Bname%3DnativeValid%5D%2Ffield=" + v
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.put(url = xnatSession.host + uri)
    if response.status_code != 200:
        raise Exception("Error setting nativeValid" % (uri,
                                                       response.status_code,
                                                       response.reason,
                                                       response.text))

def get_dicom_file(s, xnatSession):
    uri = "/data/experiments/%s/scans/%s/files" % (sesid, s)
    params = {"file_format": "DICOM", "locator": "absolutePath"}
    xnatSession.renew_httpsession()
    response = xnatSession.httpsess.get(url = xnatSession.host + uri, params = params)
    if response.status_code != 200:
        raise Exception("Error getting DICOM file (%s): %s %s %s" % (uri,
                                                                     response.status_code,
                                                                     response.reason,
                                                                     response.text))
    res = response.json()["ResultSet"]["Result"][0]
    return res["absolutePath"], res["digest"]

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def validate_dicom(s, xnatSession):
    sfile, actual = get_dicom_file(s, xnatSession)
    sfilename = os.path.basename(sfile)
    csfile = os.path.join(resdir, subdir, "%s.txt" % os.path.splitext(sfilename)[0])
    return compare_checksums(actual, csfile, sfile, "%s (%s)" % (s, sfilename))

def validate_native(xnatSession):
    zipfiles = glob.glob(os.path.join(resdir, subdir, '*.zip'))
    if len(zipfiles) != 1:
        msg = "Expected precisely one native format zip file in \"%s\", found: %s" \
            % (os.path.basename(resdir), zipfiles)
        print(msg)
        return False, msg
    zipfile = zipfiles[0]
    csfile  = zipfile.replace('.zip','.txt')
    return compare_checksums(None, csfile, zipfile, os.path.basename(zipfile))

def compare_checksums(actual, csfile, datafile, fname):
    if not os.path.exists(csfile):
        displaypath = os.path.join(os.path.basename(resdir), subdir, os.path.basename(csfile))
        msg = "%s: checksum file missing (expected location: %s)" % (fname, displaypath)
        print(msg)
        return False, msg
    print("Reading %s for expected checksum" % csfile)
    with open(csfile, 'r') as file:
        expected = re.sub(r'\s+', '', file.read())
    if not actual:
        print("Reading %s for actual checksum" % datafile)
        actual = md5(datafile)
    print("Expect checksum for %s: %s" % (fname, expected))
    print("Actual checksum for %s: %s" % (fname, actual))
    return expected == actual, "%s: checksums do not match" % fname


# Set up session
host    = os.environ['XNAT_HOST']
user    = os.environ['XNAT_USER']
passwd  = os.environ['XNAT_PASS']
xnatSession = XnatSession(username=user, password=passwd, host=host)

try:
    # Handle no checksum data (or unlocatable)
    if not resdir:
        typestr = 'DICOM checksums' if dicom else 'native image zipfile and checksum' 
        create_query(xnatSession, "Missing data", "Unable to locate %s" % typestr, \
            "Unable to locate %s for %s" % (typestr, label))
        print("Validation failed: no checksum resource directory")
        sys.exit()

    if dicom:
        # Handle no series
        if args.series is None or len(args.series) == 0:
            create_query(xnatSession, "Missing data", "No DICOM series uploaded", \
                "No DICOM series uploaded for %s" % label)
            print("Validation failed: no DICOM")
            sys.exit()

        # Perform validation
        failures = []
        for s in series:
            success, msg = validate_dicom(s, xnatSession)
            if not success:
                print("Checksum validation failed on series %s" % s)
                failures.append(msg)

        # Create query if needed
        if len(failures) > 0:
            create_query(xnatSession, "Wrong data", "Checksum validation failed", \
                "Checksum validation failed on DICOM series: %s" % ", ".join(failures))
        else:
            print("All series passed checksum validation")

    else:
       # Perform validation and create query if needed
       success, msg = validate_native(xnatSession)
       mark_native_files_valid(xnatSession, success)
       if not success:
            print(msg)
            create_query(xnatSession, "Wrong data", "Checksum validation failed", \
                "Checksum validation failed: %s" % msg)
       else:
            print("Checksum validation passed")
    
# All done
finally:
    xnatSession.close_httpsession()
