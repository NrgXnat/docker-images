# XNAT Radiomics

This will build the XNAT Radiomics (a.k.a. "metlab") images. It is split into two images to facilitate development.

The first image references shared files on the NRG internal network, and as such can only be built on a machine or VM with access to those shared files. To build an image from `Dockerfile.metlab`, the build must be run from the directory `/home/shared/NRG/mmilch/lib`. This is because there are scripts and executables in the subdirectories that are referenced by `COPY` instructions in the Dockerfile.

The second image contains a python script to generate radiomics assessor XMLs, and a wrapper shell script which runs the metlab scripts and the script which generates the assessor XMLs. It can be built anywhere.