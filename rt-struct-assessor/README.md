## Background

This container enables a workflow for the OHIF viewer as it exists now in May 2018. That viewer can read DICOM RT-STRUCT files (I think the relevant portion of the DICOM Spec is [C.8.8.5 Structure Set Module](http://dicom.nema.org/dicom/2013/output/chtml/part03/sect_C.8.html#sect_C.8.8.5)), which it expects to be stored as a resource named `RT_STRUCT` on an assessor of XSI type `icr:roiCollectionData`.

The folks working on the OHIF viewer have a custom uploader that they use to put the RT-STRUCT file into the correct place.

When we upload RT-STRUCT files to XNAT using the ordinary DICOM upload process, they get saved on a session as a new scan. This scan doesn't have a lot of the usual things scans do, like an id or a type.

## Purpose

* The command will be invoked when an RT-STRUCT scan is uploaded. (Or at least that is the hope. I don't yet know a reliabel way to trigger on these scans.)
* The container service will mount the scan's DICOM resource.
* The script that runs inside the container will read the DICOM RT-STRUCT headers and use them to write the `icr:roiCollectionData` assessor XML.
* The container service will create the assessor object from this XML, and upload the DICOM RT-STRUCT to it as a resource.
