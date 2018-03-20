#!/usr/bin/perl
# $Id: stats2xml.pl,v 1.6 2014/01/13 16:22:00 jflavin Exp $
# Copyright (c) 2007 Washington University
# Author: Kevin A. Archie <karchie@npg.wustl.edu>

use strict;
use Getopt::Long;

use lib "/usr/local/bin/fs2xml";
require FreeSurfer::Stats;

my $VC_ID = '$Id: stats2xml.pl,v 1.6 2014/01/13 16:22:00 jflavin Exp $';


my $project;
my $xnat_id;
my $xmlType;
my $fs_id;
my @t1s ;
my $validationStatus;
my $version = 0;
my $help = 0;

GetOptions('p=s' => \$project, 'x=s' => \$xnat_id, 'f=s' => \$fs_id, 't=s' => \$xmlType, 'm=s' => \@t1s, 'v' => \$version,  'h' => \$help, 'c=s' => \$validationStatus);

if ($version) {
    print STDOUT "$VC_ID\n";
    exit 0;
}


if ($help) {
    print STDERR <<EndOfHelp;
$VC_ID
Generates XNAT XML from FreeSurfer stats files
Options:

    -p <project>   Define project name (required).
    -x <XNAT ID>   Define XNAT ID of the MRSession  (required).
    -t <Freesurfer or LongitudinalFS> Define which type of XML you want to create
    -f Freesurfer ID
    -m T1 IDs
    -c Validation Status
    -h             Show this help information
    -v   Show program version
EndOfHelp
}



die "No project defined (use -p option)\n" unless defined $project;
die "No XNAT ID defined (use -x option)\n" unless defined $xnat_id;
die "No XMLTYPE defined (use -t option [Freesurfer|LongitudinalFS)\n" unless defined $xmlType;
die "No Freesurfer ID supplied for the assessor ID (use -f option)\n" unless defined $fs_id;


print STDOUT "all right then.\n";

my @provenance_fields = (
    ['prov:program', 'generating_program', 'version', 'program_version',
        'arguments', 'cmdargs'],
    ['prov:timestamp', 'timestamp'],
    ['prov:cvs', 'cvs_version'],
    ['prov:user', 'user'],
    ['prov:machine', 'hostname'],
    ['prov:platform', 'sysname'],
);

my @aseg_in_files = (
    ['segmentation volume', 'SegVolFile'],
    ['in volume', 'InVolFile'],
    ['pv volume', 'PVVolFile'],
);

my @aseg_parameters = (
    ['InVolFrame', 'InVolFrame'],
    ['ExcludeSegId', 'ExcludeSegId'],
    ['VoxelVolume_mm3', 'VoxelVolume_mm3'],
);

my @aseg_global_measures = (
    ['fs:ICV', 'eTIV'],
    ['fs:lhCortexVol','lhCortexVol'],
    ['fs:rhCortexVol','rhCortexVol'],
    ['fs:CortexVol', 'CortexVol'],
    ['fs:SubCortGrayVol', 'SubCortGrayVol'],
    ['fs:TotalGrayVol', 'TotalGrayVol'],
    ['fs:SupraTentorialVol','SupraTentorialVol'],
    ['fs:lhCorticalWhiteMatterVol','lhCorticalWhiteMatterVol'],
    ['fs:rhCorticalWhiteMatterVol', 'rhCorticalWhiteMatterVol'],
    ['fs:CorticalWhiteMatterVol','CorticalWhiteMatterVol'],
    ['fs:BrainSegVol', 'BrainSegVol'],
    ['fs:BrainSegVolNotVent', 'BrainSegVolNotVent'],
    ['fs:BrainSegVolNotVentSurf', 'BrainSegVolNotVentSurf'],
    ['fs:SupraTentorialVolNotVent', 'SupraTentorialVolNotVent'],
    ['fs:SupraTentorialVolNotVentVox', 'SupraTentorialVolNotVentVox'],
    ['fs:MaskVol', 'MaskVol'],
    ['fs:BrainSegVol-to-eTIV', 'BrainSegVol-to-eTIV'],
    ['fs:MaskVol-to-eTIV', 'MaskVol-to-eTIV'],
    ['fs:lhSurfaceHoles', 'lhSurfaceHoles'],
    ['fs:rhSurfaceHoles', 'rhSurfaceHoles'],
    ['fs:SurfaceHoles', 'SurfaceHoles'],
);

my @aseg_region_attrs = (
    ['SegId', 'SegId'],
    ['name', 'StructName']
);

my @aseg_region_measures = (
    ['fs:NVoxels', 'NVoxels'],
    ['fs:Volume', 'Volume_mm3'],
    ['fs:normMean', 'normMean'],
    ['fs:normStdDev', 'normStdDev'],
    ['fs:normMin', 'normMin'],
    ['fs:normMax', 'normMax'],
    ['fs:normRange', 'normRange'],
);


my @aparc_in_files = (
    ['annotation', 'AnnotationFile'],
);

my @aparc_parameters = ();

my @aparc_global_measures = (
    ['fs:NumVert', 'NumVert'],
    ['fs:SurfArea', 'WhiteSurfArea'],
);

my @aparc_region_attrs = (
    ['name', 'StructName'],
);

my @aparc_region_measures = (
    ['fs:NumVert', 'NumVert'],
    ['fs:SurfArea', 'SurfArea'],
    ['fs:GrayVol', 'GrayVol'],
    ['fs:ThickAvg', 'ThickAvg'],
    ['fs:ThickStd', 'ThickStd'],
    ['fs:MeanCurv', 'MeanCurv'],
    ['fs:GausCurv', 'GausCurv'],
    ['fs:FoldInd', 'FoldInd'],
    ['fs:CurvInd', 'CurvInd'],
);


# arguments:
# filename
# file type ("aseg"/"aparc")
# provenance fields (array ref)
# in_files descs (array ref)
# parameters desc (array ref)
# global measures desc (array ref)
# region attributes desc (array ref)
# region measures desc (array ref)


sub insertReconAllProvenance($$) {
    my ($XMLFILE, $scriptsDir) = @_;
    my $path_to_recon_all = $scriptsDir;
    my $recon_all_log = $path_to_recon_all."/recon-all.log";
    my $recon_all_env = $path_to_recon_all."/recon-all.env";
    my $recon_all = `grep "/recon-all" $recon_all_log | sort -u`;
    chomp($recon_all);
    my $recon_all_args = `awk  '/setenv/ {getline; print}' $recon_all_env`;
    chomp($recon_all_args);
    my $recon_all_version_str = `grep "recon-all,v" $recon_all_log | sort -u`;
    chomp($recon_all_version_str);
    my $recon_all_version = 'unknown';
    my $timestamp_str = `head -1 $recon_all_env`;
    my $timestamp = "0001-01-01T00:00:00Z";
    my @time_values = split(' ',$timestamp_str);
    chomp(@time_values);
    my $year = $time_values[5];
    my $month_str = $time_values[1];
    my %mons=('Jan'=>'01','Feb'=>'02', 'Mar'=>'03', 'Apr'=>'04', 'May'=>'05', 'Jun'=>'06', 'Jul'=>'07', 'Aug'=>'08', 'Sep'=>'09', 'Oct'=>'10', 'Nov'=>'11', 'Dec'=>'12');
    my $date = $time_values[2];
    my $time = $time_values[3];
    my $month = $mons{$month_str};
    my $user_str = `grep USER $recon_all_env | sort -u`;
    my @user = split('=',$user_str);
    chomp(@user);
    my $host_str = `grep HOSTNAME $recon_all_env | sort -u`;
    if ($host_str==''){
        $host_str = `grep HOST= $recon_all_env | sort -u`;
    }
    my @host = split('=',$host_str);
    chomp(@host);
    my $os_str = `grep OSTYPE= $recon_all_env | sort -u`;
    my @os = split('=',$os_str);
    chomp(@os);

    $timestamp = $year . "-". $month . "-" . $date ."T".$time;
    my @recon_all_info=split(/ /,$recon_all_version_str);
    chomp(@recon_all_info);
    $recon_all_version = $recon_all_info[2];
    print $XMLFILE "\t\t<prov:processStep>\n";
    print $XMLFILE "\t\t\t<prov:program version=",'"', $recon_all_version ,'" arguments="',$recon_all_args,'">', $recon_all,"</prov:program>\n";
    print $XMLFILE "\t\t\t<prov:timestamp>",$timestamp,"</prov:timestamp>\n";
    print $XMLFILE "\t\t\t<prov:cvs>",$recon_all_version_str,"</prov:cvs>\n";
    print $XMLFILE "\t\t\t<prov:user>",$user[1],"</prov:user>\n";
    print $XMLFILE "\t\t\t<prov:machine>",$host[1],"</prov:machine>\n";
    print $XMLFILE "\t\t\t<prov:platform>",$os[1],"</prov:platform>\n";
    print $XMLFILE "\t\t</prov:processStep>\n";
}

sub insertAsegProvenance($$$) {
    my ($XMLFILE, $meta, $provenance_fields) = @_;
    print $XMLFILE "\t\t<prov:processStep>\n";

    for my $tagdef (@{$provenance_fields}) {
        next unless exists $meta->{$tagdef->[1]};
        print $XMLFILE "\t\t\t<", $tagdef->[0];
        for (my $attr_idx = 2; $attr_idx <= $#{$tagdef}; $attr_idx += 2) {
            print $XMLFILE ' ', $tagdef->[$attr_idx], '="',
            $meta->{$tagdef->[$attr_idx+1]}, '"';
        }
        print $XMLFILE ">", $meta->{$tagdef->[1]}, "</", $tagdef->[0], ">\n";
    }
    print $XMLFILE "\t\t</prov:processStep>\n";
}



sub insertAparcProvenance($$$) {
    my ($XMLFILE, $aparc_meta_ref, $provenance_fields) = @_;
    my %lr = ( 'lh' => 'left', 'rh' => 'right' );
    my %aparc_meta = %$aparc_meta_ref;

    for my $hemi ( keys %lr ) {
        print XMLFILE "\t\t<prov:processStep>\n";
        my $aparc_hemi_meta = ${$aparc_meta{$hemi}};
        for my $tagdef (@{$provenance_fields}) {
            next unless exists $aparc_hemi_meta->{$tagdef->[1]};
            print $XMLFILE "\t\t\t<", $tagdef->[0];
            for (my $attr_idx = 2; $attr_idx <= $#{$tagdef}; $attr_idx += 2) {
                print $XMLFILE ' ', $tagdef->[$attr_idx], '="',
                $aparc_hemi_meta->{$tagdef->[$attr_idx+1]}, '"';
            }
        print $XMLFILE ">", $aparc_hemi_meta->{$tagdef->[1]}, "</", $tagdef->[0], ">\n";
        }
        print $XMLFILE "\t\t</prov:processStep>\n";
    }
}

sub insertAsegInFiles($$$$) {
    my ($XMLFILE, $meta, $in_files, $root_folder) = @_;

    for my $tagdef (@{$in_files}) {
        print XMLFILE "\t\t<xnat:file xsi:type=\"xnat:imageResource\" ";
        print XMLFILE 'content="', $tagdef->[0], '" ';
        print XMLFILE 'format="MGZ" ';
        print XMLFILE 'URI="', $root_folder, '/',
            # ### dir should be same as location
            # ### of aseg file instead?
        $meta->{$tagdef->[1]}, '"/>', "\n";
    }
}

sub insertAparcInFiles($$$$) {
    my ($XMLFILE, $aparc_meta_ref, $in_files, $root_folder) = @_;
    my %lr = ( 'lh' => 'left', 'rh' => 'right' );
    my %aparc_meta = %$aparc_meta_ref;
    for my $hemi ( keys %lr ) {
        my $aparc_hemi_meta = ${$aparc_meta{$hemi}};
        for my $tagdef (@{$in_files}) {
            my $path = $aparc_hemi_meta->{$tagdef->[1]}; $path =~s/^\.\.\///;
            print XMLFILE "\t\t<xnat:file xsi:type=\"xnat:imageResource\" ";
            print XMLFILE 'content="', $tagdef->[0], '" ';
            print XMLFILE 'format="MGZ" ';
            print XMLFILE 'URI="', $root_folder, '/',
                # ### dir should be same as location
                # ### of aseg file instead?
        $path, '"/>', "\n";

        }
    }
}

sub writeParameters($$$) {
    my ($XMLFILE,$meta, $parameters) =@_;
    if ($#{$parameters} >= 0) {
        for my $tagdef (@{$parameters}) {
            print $XMLFILE "\t\t<xnat:addParam name=\"$tagdef->[0]\">";
            print $XMLFILE $meta->{$tagdef->[1]};
            print $XMLFILE "</xnat:addParam>\n";
        }
    }
}

sub writeT1_IDS_Parameters($) {
    my ($XMLFILE) =@_;
    if (scalar(@t1s) > 0) {
        print $XMLFILE "\t\t<xnat:addParam name=\"INCLUDED_T1\">";
        print $XMLFILE join(',',@t1s);
        print $XMLFILE "</xnat:addParam>\n";
    }
}



sub insertAsegMeasures($$$$$$) {
    my ($XMLFILE, $meta, $results, $global_measures, $region_attrs, $region_measures) = @_;
    for my $measure (@{$global_measures}) {
        print $XMLFILE "\t<$measure->[0]>";
        my ($val, $units) = @{$results->{GLOBALS}->{$measure->[1]}};
        print $XMLFILE $val;
        print $XMLFILE "</$measure->[0]>\n";
    }

    print $XMLFILE "\t<fs:regions>\n";
    for my $region (@{$results->{REGIONS}}) {
        print XMLFILE "\t\t<fs:region";
        for my $attr (@{$region_attrs}) {
                print XMLFILE " $attr->[0]=\"$region->{$attr->[1]}\"";
        }

        # hemisphere is a little complicated, sadly.
        my $hemisphere;
        if ($region->{StructName} =~ /\ALeft-/) {
            $hemisphere = 'left';
        } elsif ($region->{StructName} =~ /\ARight-/) {
            $hemisphere = 'right';
        }
        print $XMLFILE " hemisphere=\"$hemisphere\"" if defined $hemisphere;

        print $XMLFILE ">\n";

        for my $measure (@{$region_measures}) {
            print $XMLFILE "\t\t\t<$measure->[0]>";
            print $XMLFILE $region->{$measure->[1]};
            print $XMLFILE "</$measure->[0]>\n";
        }
        print $XMLFILE "\t\t</fs:region>\n";
    }
    print $XMLFILE "\t</fs:regions>\n";
}

sub insertAparcMeasures($$$$$) {
    my ($XMLFILE,  $aparc_results_ref, $global_measures, $region_attrs, $region_measures) = @_;
    my %lr = ( 'lh' => 'left', 'rh' => 'right' );
    my %aparc_results = %$aparc_results_ref;

    for my $hemi ( keys %lr ) {
        my $aparc_hemi_results = ${$aparc_results{$hemi}};

        print XMLFILE "\t<fs:hemisphere name=\"".$lr{$hemi} ."\">\n";
        for my $measure (@{$global_measures}) {
            print $XMLFILE "\t<$measure->[0]>";
            my ($val, $units) = @{$aparc_hemi_results->{GLOBALS}->{$measure->[1]}};
            print $XMLFILE $val;
            print $XMLFILE "</$measure->[0]>\n";
        }
        print $XMLFILE "\t<fs:regions>\n";
        for my $region (@{$aparc_hemi_results->{REGIONS}}) {
        print $XMLFILE "\t\t<fs:region";
        for my $attr (@{$region_attrs}) {
            print $XMLFILE " $attr->[0]=\"$region->{$attr->[1]}\"";
        }
        print $XMLFILE ">\n";

        for my $measure (@{$region_measures}) {
            print $XMLFILE "\t\t\t<$measure->[0]>";
            print $XMLFILE $region->{$measure->[1]};
            print $XMLFILE "</$measure->[0]>\n";
        }
        print $XMLFILE "\t\t</fs:region>\n";
        }
        print $XMLFILE "\t</fs:regions>\n";

        print $XMLFILE "\t</fs:hemisphere>\n";
    }
}


sub createXMLHeader {
    my $XMLFILE = shift;
    my $subjectLabel = shift;
    my $cur_time = gmtime;
    # Start printing the XML document.
    print $XMLFILE <<EndOfHeader;
<?xml version="1.0" encoding="UTF-8"?>
<!-- XNAT XML generated by $VC_ID on $cur_time -->
<fs:$xmlType xmlns:xnat="http://nrg.wustl.edu/xnat"
xmlns:prov="http://www.nbirn.net/prov"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:fs="http://nrg.wustl.edu/fs"
xsi:schemaLocation="http://nrg.wustl.edu/fs ../schemas/fs/fs.xsd"
ID="${fs_id}" label="$subjectLabel" project="$project"
EndOfHeader
    print $XMLFILE ">\n";
}


sub printToXML {
    my $XMLFILE = shift;
    my $xmlElement = shift;
    my $value = shift;
    print $XMLFILE "\t<${xmlElement}>$value</${xmlElement}>\n";
}


sub createValidationStatus {
    my $XMLFILE = shift;
    my $validationStat = shift;
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime time;
    $year += 1900;
    $mon += 1;
    my $monStr=$mon;
    my $mdayStr=$mday;
    if ($mon < 10) {
        $monStr="0".$mon
    }
    if ($mday < 10) {
        $mdayStr="0".$mday
    }
    print $XMLFILE "\t<xnat:validation status=\"".$validationStat."\">\n";
    print $XMLFILE "\t<xnat:method>Manual Edit</xnat:method>\n";
    print $XMLFILE "\t<xnat:date>$year-$monStr-$mdayStr</xnat:date>\n";
    print $XMLFILE "\t</xnat:validation>\n";
}


sub printToXMLOpenTag {
    my $XMLFILE = shift;
    my $tag = shift;
        print $XMLFILE "\t<".$tag.">\n";
}

sub printToXMLCloseTag {
    my $XMLFILE = shift;
    my $tag = shift;
        print $XMLFILE "\t</".$tag.">\n";
}

sub getFreesurferVersion($) {
    my ($path) = @_;
    my $build_file= $path."/build-stamp.txt";
    open (BUILDFILE, $build_file) || die ("Could not open file <br> $!");
    my $text = <BUILDFILE>;
    close (BUILDFILE);
    chomp($text);
    return $text;
}


for my $dir (@ARGV) {
    print STDOUT "Processing $dir...";
    $dir =~s/\/$//;
    my $root_folder = $dir;
    $root_folder =~s/\/stats//;

    #my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
    #$year += 1900;
    #my $datetime = ${year}.${mon}.${mday};

    my $xmlfile = "${xnat_id}_freesurfer5.xml";
    open(XMLFILE, ">$xmlfile") || die "Can't open XML file $xmlfile: $!";

    my $asegResults = Stats::read($dir."/aseg.stats");
    my $asegMeta = $asegResults->{METADATA};

    my %aparc_results = ();
    my %aparc_meta = ();
    my %lr = ( 'lh' => 'left', 'rh' => 'right' );
    my $lh_aparc_results = Stats::read($dir."/lh.aparc.stats");
    my $rh_aparc_results = Stats::read($dir."/rh.aparc.stats");
    $aparc_results{"lh"} = \$lh_aparc_results; #ref to a record
    $aparc_results{"rh"} = \$rh_aparc_results; #ref to a record
    my $meta_lh_aparc = $lh_aparc_results->{METADATA}; #ref to a hash
    my $meta_rh_aparc = $rh_aparc_results->{METADATA}; #ref to a hash
    $aparc_meta{"lh"} = \$meta_lh_aparc;
    $aparc_meta{"rh"} = \$meta_rh_aparc;
    my $aparcMetaData = $lh_aparc_results->{METADATA};

    createXMLHeader(*XMLFILE,$fs_id);
    my $exptdate = undef;
    if (defined $asegMeta->{exptdate}) {
        $exptdate = $asegMeta->{exptdate};
    }elsif (defined $aparcMetaData->{exptdate} ) {
        $exptdate = $aparcMetaData->{exptdate};
    }

    if (defined $exptdate) {
        printToXML(*XMLFILE,"xnat:date",$exptdate);
    }
    if (defined $validationStatus) {
        createValidationStatus(*XMLFILE,$validationStatus);
    }

    printToXMLOpenTag(*XMLFILE,"xnat:provenance");
    insertReconAllProvenance(*XMLFILE,$root_folder."/scripts");
    insertAsegProvenance(*XMLFILE, $asegMeta,\@provenance_fields);
    insertAparcProvenance(*XMLFILE, \%aparc_meta, \@provenance_fields);
    printToXMLCloseTag(*XMLFILE,"xnat:provenance");

    #printToXMLOpenTag(*XMLFILE,"xnat:in");

    # insertAsegInFiles(*XMLFILE, $asegMeta,\@aseg_in_files, $root_folder);
    # insertAparcInFiles(*XMLFILE, \%aparc_meta,\@aparc_in_files,$root_folder);
    # printToXMLCloseTag(*XMLFILE,"xnat:in");
    printToXML(*XMLFILE,"xnat:imageSession_ID",$xnat_id);

    if( @aseg_parameters >= 0) {
        printToXMLOpenTag(*XMLFILE,"xnat:parameters");
        writeParameters(*XMLFILE, $asegMeta, \@aseg_parameters);
        writeT1_IDS_Parameters(*XMLFILE);
        printToXMLCloseTag(*XMLFILE,"xnat:parameters");
    }else {
        printToXMLOpenTag(*XMLFILE,"xnat:parameters");
        writeT1_IDS_Parameters(*XMLFILE );
        printToXMLCloseTag(*XMLFILE,"xnat:parameters");
    }

    my $fs_version = getFreesurferVersion($root_folder."/scripts");
    printToXML(*XMLFILE,"fs:fs_version",$fs_version);


    printToXMLOpenTag(*XMLFILE,"fs:measures");
    printToXMLOpenTag(*XMLFILE,"fs:volumetric");
    insertAsegMeasures(*XMLFILE, $asegMeta, $asegResults,\@aseg_global_measures,\@aseg_region_attrs, \@aseg_region_measures) ;
    printToXMLCloseTag(*XMLFILE,"fs:volumetric");
    printToXMLOpenTag(*XMLFILE,"fs:surface");

    insertAparcMeasures(*XMLFILE,  \%aparc_results,\@aparc_global_measures,\@aparc_region_attrs, \@aparc_region_measures);
    printToXMLCloseTag(*XMLFILE,"fs:surface");
    printToXMLCloseTag(*XMLFILE,"fs:measures");

    printToXMLCloseTag(*XMLFILE,"fs:$xmlType");


    close XMLFILE || print STDERR "Unable to close $xmlfile: $!";

    print STDOUT "done.\n";}

exit 0;
