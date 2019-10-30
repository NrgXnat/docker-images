#!/bin/bash

dir=$1
sesId=$2
scanId=$3

cd $dir

cat > scan.xml << EOF
<xnat:MRScan xmlns:arc="http://nrg.wustl.edu/arc" xmlns:val="http://nrg.wustl.edu/val" xmlns:pipe="http://nrg.wustl.edu/pipe" xmlns:wrk="http://nrg.wustl.edu/workflow" xmlns:scr="http://nrg.wustl.edu/scr" xmlns:xdat="http://nrg.wustl.edu/security" xmlns:cat="http://nrg.wustl.edu/catalog" xmlns:prov="http://www.nbirn.net/prov" xmlns:xnat="http://nrg.wustl.edu/xnat" xmlns:xnat_a="http://nrg.wustl.edu/xnat_assessments" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  ID="${scanId}cont" type="containerDerived" xsi:schemaLocation="http://nrg.wustl.edu/workflow http://localhost/schemas/workflow.xsd http://nrg.wustl.edu/catalog http://localhost/schemas/catalog.xsd http://nrg.wustl.edu/pipe http://localhost/schemas/repository.xsd http://nrg.wustl.edu/scr http://localhost/schemas/screeningAssessment.xsd http://nrg.wustl.edu/arc http://localhost/schemas/project.xsd http://nrg.wustl.edu/xnat http://localhost/schemas/xnat.xsd http://nrg.wustl.edu/val http://localhost/schemas/protocolValidation.xsd http://nrg.wustl.edu/xnat_assessments http://localhost/schemas/assessments.xsd http://www.nbirn.net/prov http://localhost/schemas/birnprov.xsd http://nrg.wustl.edu/security http://localhost/schemas/security.xsd">
<xnat:image_session_ID>$sesId</xnat:image_session_ID>
<xnat:note>3</xnat:note>
<xnat:series_description>containerUpload</xnat:series_description>
<xnat:modality>T1w</xnat:modality>
<xnat:parameters>
<xnat:tr>2.4</xnat:tr>
<xnat:te>0.00316</xnat:te>
<xnat:ti>1.0</xnat:ti>
<xnat:flip>8</xnat:flip>
<xnat:sequence>GR_IR</xnat:sequence>
<xnat:imageType>ORIGINAL\\PRIMARY\\M\\ND\\NORM</xnat:imageType>
<xnat:seqVariant>SP_MP_OSP</xnat:seqVariant>
<xnat:phaseEncodingDirection>i-</xnat:phaseEncodingDirection>
<xnat:acqTime>2013-04-29T00:00:00</xnat:acqTime>
</xnat:parameters>
</xnat:MRScan>
EOF

echo copying DICOM
mkdir -p DICOM
cp -v /sample_data/DICOM/* DICOM/

echo done
