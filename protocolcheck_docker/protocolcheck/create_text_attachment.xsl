<!--
  ~ pipeline: create_text_attachment.xsl
  ~ XNAT http://www.xnat.org
  ~ Copyright (c) 2018, Washington University School of Medicine
  ~ All Rights Reserved
  ~
  ~ Released under the Simplified BSD.
  -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:val="http://nrg.wustl.edu/val" xmlns:xnat="http://nrg.wustl.edu/xnat" xmlns:svrl="http://purl.oclc.org/dsdl/svrl" xmlns:nrgxsl="http://nrg.wustl.edu/validate" xmlns:prov="http://www.nbirn.net/prov" xmlns:ext="org.nrg.validate.utils.ProvenanceUtils">
<xsl:output method="text" indent="yes" encoding="US-ASCII" />


<xsl:variable name="tab" select="'&#09;'" />

<xsl:variable name="newline" select="'&#13;&#10;'" />

<xsl:param name="xnatserver"/>


<xsl:template match="/">

<xsl:value-of select="$xnatserver"/> VALIDATION REPORT
---------------------------------------------------------------


Experiment : <xsl:value-of select="/svrl:schematron-output/svrl:successful-report[@id='expt_label']/svrl:text"/>

Project :   <xsl:value-of select="/svrl:schematron-output/svrl:successful-report[@id='expt_project']/svrl:text"/>

Validation Date: <xsl:value-of select="ext:GetDate()"/>

Overall protocol check status : <xsl:choose><xsl:when test="count(/svrl:schematron-output/svrl:failed-assert)>0">FAIL</xsl:when><xsl:otherwise>PASS</xsl:otherwise></xsl:choose>


<xsl:if test="count(//nrgxsl:acquisition)>0">

Failure causes:
---------------
	<xsl:for-each select="//nrgxsl:acquisition">
*  <xsl:value-of select="normalize-space(@cause-id)"/> :	<xsl:choose><xsl:when test="name(../..)='svrl:failed-assert'">FAIL</xsl:when>
			      <xsl:otherwise>PASS</xsl:otherwise>
			</xsl:choose>

<xsl:value-of select="$newline"/>
<xsl:value-of select="$tab"/><xsl:value-of select="normalize-space(.)"/>
	</xsl:for-each> 
 </xsl:if>    


SCAN LEVEL CHECK
----------------
		 <xsl:for-each select="//nrgxsl:scans">
			<xsl:call-template name="process-scan">
				<xsl:with-param name="scan-id" select="normalize-space(.)" />

			</xsl:call-template>
<xsl:value-of select="$newline"/>

	 	  </xsl:for-each>
</xsl:template>

<xsl:template name="process-scan">
	<xsl:param name="scan-id"/>
 <xsl:choose>
 <xsl:when test="count(//nrgxsl:scan[@id=$scan-id])>0">

* SCAN <xsl:value-of select="$scan-id"/>:<xsl:choose><xsl:when test="count(/svrl:schematron-output/svrl:failed-assert/svrl:text/nrgxsl:scan[@id=$scan-id])>0">FAIL</xsl:when><xsl:otherwise>PASS</xsl:otherwise></xsl:choose>


<xsl:for-each select="//nrgxsl:scan[@id=$scan-id]">
<xsl:value-of select="$tab"/>

	o <xsl:value-of select="@cause-id"/>:<xsl:choose>
			      <xsl:when test="name(../..)='svrl:failed-assert'">FAIL
				<xsl:value-of select="$newline"/>
<xsl:value-of select="$tab"/>
<xsl:value-of select="$tab"/>
	<xsl:value-of select="."/>
<xsl:value-of select="$newline"/>
	
			      
			      </xsl:when>
			      <xsl:otherwise>PASS <xsl:value-of select="$newline"/>
</xsl:otherwise>
	   </xsl:choose>
			</xsl:for-each> 
</xsl:when>
<xsl:otherwise>
* SCAN <xsl:value-of select="$scan-id"/>:No checks specified
</xsl:otherwise>
</xsl:choose>
</xsl:template>

</xsl:stylesheet>
