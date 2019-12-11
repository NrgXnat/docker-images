import argparse
import sys
import os
import hashlib
from xnatSession import XnatSession

parser = argparse.ArgumentParser(description="Run checksum validation")

parser.add_argument("--sessionId", help="Session ID", required=True)
parser.add_argument("--sessionLabel", help="Session Label", required=True)
parser.add_argument("--assignTo", help="Assign query to this user", required=True)
parser.add_argument("--checksumResource", help="Checksum file resource directory", required=True)
parser.add_argument("--series", action="append", help="DICOM series XNAT ID", required=False)

args = parser.parse_args()

sesid       = args.sessionId
label       = args.sessionLabel
assignTo    = args.assignTo
series      = args.series
resdir      = args.checksumResource

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


def validate(s, xnatSession):
    sfile, actual = get_dicom_file(s, xnatSession)
    if not actual:
        print("Reading %s for actual checksum" % sfile)
        actual = md5(sfile)
    sfilename = os.path.basename(sfile)
    csfile = os.path.join(resdir, "%s.txt" % os.path.splitext(sfilename)[0])
    print("Reading %s for expected checksum" % csfile)
    with open(csfile, 'r') as file:
        expected = file.read()
    print("Expect checksum for %s: %s" % (sfilename, expected))
    print("Actual checksum for %s: %s" % (sfilename, actual))
    return expected == actual, sfilename

try:
    # Set up session
    host    = os.environ['XNAT_HOST']
    user    = os.environ['XNAT_USER']
    passwd  = os.environ['XNAT_PASS']
    xnatSession = XnatSession(username=user, password=passwd, host=host)

    # Handle no series
    if args.series is None or len(args.series) == 0:
        create_query(xnatSession, "Missing data", "No DICOM series uploaded", \
            "No DICOM series uploaded for %s" % label)
        print("Validation failed: no DICOM")
        sys.exit()

    # Perform validation
    failures = []
    for s in series:
        success, sfilename = validate(s, xnatSession)
        if not success:
            print("Checksum validation failed on series %s" % s)
            failures.append("%s (%s)" % (s, sfilename))

    # Create query if needed
    if len(failures) > 0:
        create_query(xnatSession, "Wrong data", "Checksum validation failed", \
            "Checksum validation failed on DICOM series: %s" % ", ".join(failures))
    else:
        print("All series passed checksum validation")
    
# All done
finally:
    xnatSession.close_httpsession()
