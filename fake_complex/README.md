# XNAT Pyradiomics Wrapper

This image provides wrapper scripts around the `pyradimics` command-line interface for use with the XNAT Container Service.

`pyradiomics` needs an image and a mask in NRRD format. You can generate these using the `xnat/plastimatch` container, which works on DICOM for both the image and the mask as an RTStruct.
