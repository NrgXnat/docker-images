<?xml version="1.0" encoding="UTF-8"?>
<?altova_samplexml file:///D:/Schematron/XNAT/protocol.report.xml?>
<!--
  ~ pipeline: generate_sch_rule_report.xsl
  ~ XNAT http://www.xnat.org
  ~ Copyright (c) 2018, Washington University School of Medicine
  ~ All Rights Reserved
  ~
  ~ Released under the Simplified BSD.
  -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:iso="http://purl.oclc.org/dsdl/schematron" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:val="http://nrg.wustl.edu/val" xmlns:xnat="http://nrg.wustl.edu/xnat" xmlns:svrl="http://purl.oclc.org/dsdl/svrl" xmlns:nrgxsl="http://nrg.wustl.edu/validate" xmlns:prov="http://www.nbirn.net/prov" xmlns:ext="org.nrg.validate.utils.ProvenanceUtils">
<xsl:output method="html" indent="yes" />
<!-- Pass the following parameters on the commandline. These are used for provenance-->
<xsl:param name="schematronFileName"/>
<xsl:param name="project"/>

 
<xsl:param name="now-date"><xsl:value-of select="ext:GetDate()"/></xsl:param>
<xsl:param name="now-time"><xsl:value-of select="ext:GetTime()"/></xsl:param>

<xsl:template match="/">
<xsl:message>Generating Report Document</xsl:message>
<xsl:message>ReportFileName <xsl:value-of select="$schematronFileName" /></xsl:message>

<html>

<p>CNDA Project: <b><xsl:value-of select="$project" /></b> </p>

<p>Schematron File Name: <xsl:value-of select="$schematronFileName" /> </p>
<br></br>

Report Generation Date: <xsl:value-of select="$now-date"/> Time: <xsl:value-of select="$now-time"/>
<br></br>
<br></br>

<b>Note</b> 

<table>
<tr>
<TH> Measure </TH> <TH> Unit </TH>
</tr>
<tr>
<td>Echo Time (TE)</td> <td> milli-sec </td>
</tr>
<tr>
<td>Repetition Time (TR)</td> <td> milli-sec </td>
</tr>
<tr>
<td>Inversion Time (TI)</td> <td> milli-sec </td>
</tr>
<tr>
<td>Bandwidth </td> <td> Hz/px </td>
</tr>

</table>
		 <xsl:for-each select="/iso:schema/iso:pattern[@id='Scan']/iso:rule">
		 
			<xsl:call-template name="process-scan-rule">
				<xsl:with-param name="scan-type" select="normalize-space(@context)" />
			</xsl:call-template>
	 	  </xsl:for-each>

</html>

	<xsl:message>DONE</xsl:message>
</xsl:template>

<xsl:template name="process-scan-rule">
	<xsl:param name="scan-type"/>
<br></br>

  <xsl:variable name="cleanScanType">
    <xsl:call-template name="string-replace-all">
      <xsl:with-param name="text" select="$scan-type" />
      <xsl:with-param name="replace" select="'/xnat:MRSession/xnat:scans/xnat:scan[@type='" />
      <xsl:with-param name="by" select="''" />
    </xsl:call-template>
  </xsl:variable>


  <xsl:variable name="cleanedScanType">
    <xsl:call-template name="string-replace-all">
      <xsl:with-param name="text" select="$cleanScanType" />
      <xsl:with-param name="replace" select="']'" />
      <xsl:with-param name="by" select="''" />
    </xsl:call-template>
  </xsl:variable>

	
<b> Scan Type: <xsl:value-of select="$cleanedScanType" /> </b>	
<br></br>
<br></br>

<table>
<tr>
 <TH>Check </TH> <TH>Condition </TH>
</tr>
<xsl:for-each select="./iso:assert">
<TR>
<TD><xsl:value-of select="normalize-space(./nrgxsl:scan/nrgxsl:cause-id/text())"/> </TD> <TD><xsl:value-of select="normalize-space(@test)"/> </TD> 
</TR>
</xsl:for-each> 

</table>
</xsl:template>

<xsl:template name="string-replace-all">
    <xsl:param name="text" />
    <xsl:param name="replace" />
    <xsl:param name="by" />
    <xsl:choose>
      <xsl:when test="contains($text, $replace)">
        <xsl:value-of select="substring-before($text,$replace)" />
        <xsl:value-of select="$by" />
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text"
          select="substring-after($text,$replace)" />
          <xsl:with-param name="replace" select="$replace" />
          <xsl:with-param name="by" select="$by" />
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$text" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>


</xsl:stylesheet>

