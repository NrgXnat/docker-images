# XNAT Radiomics

This will build the XNAT Radiomics (a.k.a. "rtlab", née "metlab") images.

## Final image: xnat/rtlab

The last image in the sequence is tagged as `xnat/rtlab`. This is the one that actually gets executed by the end user.

To build it, one need only do an ordinary `docker build -t xnat/rtlab:<some version> .` from the `radiomics/rtlab` directory in this repo. It builds atop the `xnat/rtlab-base` image; the instructions to build this latter image are below.

This image is very thin, and adds only a few scripts to the base image:
* `create-radiomics-assessor.py` - Reads some of the outputs of the rtlab scripts, generates proper `radm:radiomics` assessor XMLs for them, and uploads them as new assessors.
* `run.sh` - Runs the `rtlab_wrapper.sh` script from the base image, then generates/uploads assessors with `create-radiomics-assessor.py`.

## Base image: xnat/rtlab-base

This image builds atop `xnat/rtlab-base:nodeps.<some version>`. It is built from `Dockerfile.rtlab-base`. It *must* be built on the NRG internal network, because it relies on files in a shared drive hosted there.

To build an image from `Dockerfile.rtlab-base`,

* SSH to an NRG VM with docker installed. (Currently, cnda-dev-flavn2.nrg.mir can be used for this purpose.)
* Clone this repo onto that machine, or at the least get `Dockerfile.rtlab-base` there. (Currently, the repo is on cnda-dev-flavn2.nrg.mir in /tmp. You may have to fetch recent changes.)
* Ensure that the image referenced in the `FROM` line of `Dockerfile.rtlab-base`, `xnat/rtlab-base:nodeps.<some version>`, exists on the machine. If it does not, either build it using the instructions below, or modify the `FROM` line to use an updated version of this image.
* `cd` to the directory `/home/shared/NRG/mmilch/lib/rtlab`
* Build the image with the command `docker build -t xnat/rtlab-base:<some version> -f /path/to/Dockerfile.rtlab-base .`
* Push it to docker hub

Then you will want to rebuild the `xnat/rtlab` image. You will have to modify its `Dockerfile` to reference the newly built `xnat/rtlab-base` image.

## Even Baser Image: xnat/rtlab-base:nodeps

I added this image to the build sequence because it is big and takes a long time to run. I didn't want to have to re-run this one long step every time I rebuilt the `xnat/rtlab-base` image, so I saved it as its own image.

It is built from `Dockerfile.rtlab-base-nodeps`. It can be built anywhere, but it must be present on the machine where you want to build `xnat/rtlab-base`.
