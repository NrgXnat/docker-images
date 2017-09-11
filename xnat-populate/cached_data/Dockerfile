FROM greppy/xnat-populate:2.0-uncached

MAINTAINER Charlie Moore <moore.c@wustl.edu>

RUN cd xnat_populate && \
    groovy PopulateXnat.groovy -ch -d allData.txt -s localhost -u admin -p admin && \
    cd data && \
    rm -R -- */
