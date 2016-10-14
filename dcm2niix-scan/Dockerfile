FROM neurodebian:nd14.04
RUN apt-get -y update && apt-get -y install dcm2niix
LABEL org.nrg.commands="[{\"name\": \"dcm2niix scan\", \"description\": \"Runs dcm2niix on an XNAT scan's DICOM resource\", \"docker-image\": \"xnat/dcm2niix-scan\", \"run\": {\"command-line\": \"dcm2niix -o /output /input\", \"mounts\": [{\"name\": \"dicom-in\", \"type\": \"input\", \"path\": \"/input\", \"file-input\": \"scan\", \"resource\": \"DICOM\"}, {\"name\": \"nifti-out\", \"type\": \"output\", \"path\": \"/output\", \"file-input\": \"scan\", \"resource\": \"NIFTI\" }]}, \"inputs\": [{\"name\": \"scan\", \"description\": \"Input scan\", \"type\": \"Scan\"}]}]"

