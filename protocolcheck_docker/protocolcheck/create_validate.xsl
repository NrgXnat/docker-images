<?xml version="1.0" encoding="UTF-8"?>
<?altova_samplexml file:///D:/Schematron/XNAT/protocol.report.xml?>
<!--
  ~ pipeline: create_validate.xsl
  ~ XNAT http://www.xnat.org
  ~ Copyright (c) 2018, Washington University School of Medicine
  ~ All Rights Reserved
  ~
  ~ Released under the Simplified BSD.
  -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:val="http://nrg.wustl.edu/val" xmlns:xnat="http://nrg.wustl.edu/xnat" xmlns:svrl="http://purl.oclc.org/dsdl/svrl" xmlns:nrgxsl="http://nrg.wustl.edu/validate" xmlns:prov="http://www.nbirn.net/prov" xmlns:ext="org.nrg.validate.utils.ProvenanceUtils">
<xsl:output method="xml" indent="yes" />
<!-- Pass the following parameters on the commandline. These are used for provenance-->
<xsl:param name="reportfilename"/>
<xsl:param name="rulefilename"/>
<xsl:param name="rulexslfilename"/>
<xsl:param name="xslfilename"/>
<xsl:param name="uri_content"/>


<xsl:param name="experimentfilename"/>
<xsl:param name="validationfilename"/>
<xsl:param name="validationxslfilename"/>
<xsl:param name="validation_id"/>

 
<xsl:param name="now-date"><xsl:value-of select="ext:GetDate()"/></xsl:param>
<xsl:param name="now-time"><xsl:value-of select="ext:GetTime()"/></xsl:param>
 <xsl:param name="xml-dateTime"><xsl:value-of select="concat($now-date,'T',$now-time)"/></xsl:param>
<xsl:template match="/">
<xsl:message>Generating Validation Document</xsl:message>
<xsl:message>ReportFileName <xsl:value-of select="$reportfilename" /></xsl:message>
<xsl:message>RuleFileName <xsl:value-of select="$rulefilename" /></xsl:message>
<xsl:message>RuleXSLFileName <xsl:value-of select="$rulexslfilename" /></xsl:message>
<xsl:message>XSLFileName <xsl:value-of select="$xslfilename" /></xsl:message>
<xsl:message>ExperimentFileName <xsl:value-of select="$experimentfilename" /></xsl:message>
<xsl:message>ValidationFileName <xsl:value-of select="$validationfilename" /></xsl:message>
<xsl:message>ValidationXSLFileName <xsl:value-of select="$validationxslfilename" /></xsl:message>


	<val:ProtocolVal>
<!--	<xsl:attribute name="ID">
       <xsl:value-of select="$validation_id"/>
	</xsl:attribute> -->
	<xsl:attribute name="project">
       <xsl:value-of select="/svrl:schematron-output/svrl:successful-report[@id='expt_project']/svrl:text"/>
	</xsl:attribute>
	<xnat:date><xsl:value-of select="$now-date"/></xnat:date>
	<xnat:time><xsl:value-of select="$now-time"/></xnat:time>
	<xnat:provenance>
<prov:processStep>
<prov:program>
				<xsl:attribute name="arguments"><xsl:value-of select="concat('-o ', $rulexslfilename,'  ',  $rulefilename, '   ', $xslfilename)"></xsl:value-of></xsl:attribute>
 validation-transform	
</prov:program>
				<prov:timestamp><xsl:value-of select="$xml-dateTime"/></prov:timestamp>
				<prov:user><xsl:value-of select="ext:GetUser()"/></prov:user>
				<prov:machine><xsl:value-of select="ext:GetHostName()"/></prov:machine>
				<prov:platform>
					<xsl:attribute name="version"><xsl:value-of select="ext:GetOsVersion()"/></xsl:attribute>
				<xsl:value-of select="ext:GetOsName()"/></prov:platform>
</prov:processStep>	
<prov:processStep>
<prov:program>
				<xsl:attribute name="arguments"><xsl:value-of select="concat('-o ', $reportfilename,'  ',  $experimentfilename, '   ', $xslfilename)"></xsl:value-of></xsl:attribute>
 validation-transform	
</prov:program>
				<prov:timestamp><xsl:value-of select="$xml-dateTime"/></prov:timestamp>
				<prov:user><xsl:value-of select="ext:GetUser()"/></prov:user>
				<prov:machine><xsl:value-of select="ext:GetHostName()"/></prov:machine>
				<prov:platform>
					<xsl:attribute name="version"><xsl:value-of select="ext:GetOsVersion()"/></xsl:attribute>
				<xsl:value-of select="ext:GetOsName()"/></prov:platform>
</prov:processStep>	
<prov:processStep>
<prov:program>
				<xsl:attribute name="arguments"><xsl:value-of select="concat('-o ', $validationfilename,'   ', $reportfilename,'  ', $validationxslfilename,' rulefilename=',$rulefilename,' reportfilename=',$reportfilename,' rulexslfilename=',$rulexslfilename,' experimentfilename=',$experimentfilename,' validationfilename=',$validationfilename,' xslfilename=',$xslfilename,' validationxslfilename=',$validationxslfilename,' uri_content=',$uri_content)"/></xsl:attribute>
validation-transform
</prov:program>
				<prov:timestamp><xsl:value-of select="$xml-dateTime"/></prov:timestamp>
				<prov:user><xsl:value-of select="ext:GetUser()"/></prov:user>
				<prov:machine><xsl:value-of select="ext:GetHostName()"/></prov:machine>
				<prov:platform>
					<xsl:attribute name="version"><xsl:value-of select="ext:GetOsVersion()"/></xsl:attribute>
				<xsl:value-of select="ext:GetOsName()"/></prov:platform>
</prov:processStep>	
	</xnat:provenance>
	<xnat:imageSession_ID>
			<xsl:value-of select="/svrl:schematron-output/svrl:successful-report[@id='expt_id']/svrl:text"/>
		</xnat:imageSession_ID>
	<val:check>
	    <xsl:choose>
		<xsl:when test="count(/svrl:schematron-output/svrl:failed-assert)>0">
				<xsl:attribute name="status">fail</xsl:attribute>
		</xsl:when>		
		<xsl:otherwise>
				<xsl:attribute name="status">pass</xsl:attribute>
		</xsl:otherwise>
	   </xsl:choose>

		<xsl:if test="count(//nrgxsl:acquisition)>0">
			<val:conditions>
					<xsl:for-each select="//nrgxsl:acquisition">
					   <val:condition >
					   <xsl:attribute name="ID"><xsl:value-of select="normalize-space(@cause-id)"/></xsl:attribute>
			 <xsl:if test="@xmlpath"><xsl:attribute name="xmlpath"><xsl:value-of select="normalize-space(@xmlpath)"/>
</xsl:attribute></xsl:if>

			<xsl:choose>
			      <xsl:when test="name(../..)='svrl:failed-assert'">
				<xsl:attribute name="status">fail</xsl:attribute>
			      </xsl:when>
				<xsl:otherwise>
				<xsl:attribute name="status">pass</xsl:attribute>
				</xsl:otherwise>
				</xsl:choose>

			 <val:verified>
			 <xsl:value-of select="normalize-space(../../@test)"/>
			 </val:verified>
			 <val:diagnosis>
			<xsl:value-of select="normalize-space(.)"/>
			 </val:diagnosis>

					   </val:condition>
					</xsl:for-each> 
	 	       </val:conditions>
	 	   </xsl:if>    
	</val:check>

<val:scans>
		 <xsl:for-each select="//nrgxsl:scans">
			<xsl:call-template name="process-scan">
				<xsl:with-param name="scan-id" select="normalize-space(.)" />
			</xsl:call-template>
	 	  </xsl:for-each>
</val:scans>	
	</val:ProtocolVal>
	<xsl:message>DONE</xsl:message>
</xsl:template>

<xsl:template name="process-scan">
	<xsl:param name="scan-id"/>
	

	    <val:scan_check SCAN_ID="{$scan-id}">
		<xsl:choose>
			      <xsl:when test="count(//nrgxsl:scan[@id=$scan-id])=0">
				<xsl:attribute name="status">No checks defined</xsl:attribute>
			      </xsl:when>	
			      <xsl:otherwise>
			      <xsl:choose>
			      <xsl:when test="count(/svrl:schematron-output/svrl:failed-assert/svrl:text/nrgxsl:scan[@id=$scan-id])>0">
				<xsl:attribute name="status">fail</xsl:attribute>
			       </xsl:when>
			       <xsl:otherwise>
				<xsl:attribute name="status">pass</xsl:attribute>
			       </xsl:otherwise>
	   		       </xsl:choose>
			       </xsl:otherwise>
		</xsl:choose>	       
		<val:conditions>
			<xsl:for-each select="//nrgxsl:scan[@id=$scan-id]">
			 <val:condition>
			<xsl:attribute name="ID"><xsl:value-of select="normalize-space(@cause-id)"/>
</xsl:attribute>

		<xsl:choose>
			      <xsl:when test="name(../..)='svrl:failed-assert'">
				<xsl:attribute name="status">fail</xsl:attribute>
		</xsl:when>
		<xsl:otherwise>
				<xsl:attribute name="status">pass</xsl:attribute>
		</xsl:otherwise>
	   </xsl:choose>
			<xsl:if test="@xmlpath"><xsl:attribute name="xmlpath"><xsl:value-of select="normalize-space(@xmlpath)"/>
</xsl:attribute></xsl:if>

			 <val:verified>
			 <xsl:value-of select="normalize-space(../../@test)"/>
			 </val:verified>
			 <val:diagnosis>
			<xsl:value-of select="normalize-space(.)"/>
			 </val:diagnosis>

			</val:condition>
			</xsl:for-each> 
		</val:conditions>


	</val:scan_check>
	
	
</xsl:template>

</xsl:stylesheet>
