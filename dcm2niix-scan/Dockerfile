FROM neurodebian:nd14.04
RUN apt-get -y update && apt-get -y install dcm2niix
LABEL org.nrg.commands="[{\"name\":\"dcm2niix-scan\",\"description\":\"Run dcm2niix on a scan's DICOMs\",\"mounts-in\":[{\"name\":\"DICOM\",\"remote-path\":\"/input\"}],\"mounts-out\":[{\"name\":\"NIFTI\",\"remote-path\":\"/output\"}],\"run-template\":[\"dcm2niix\",\"-o\",\"/output\",\"/input\"]}]"

