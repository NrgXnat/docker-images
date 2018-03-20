# $Id: Stats.pm,v 1.1 2007/03/15 21:04:17 karchie Exp $
# Support for reading FreeSurf ASEG/APARC stats files
# Copyright (c) 2007 Washington University
# Author: Kevin A. Archie <karchie@npg.wustl.edu>

package Stats;

require Exporter;

@ISA = qw(Exporter);
@EXPORT = qw(read);

sub read($);

=head1 NAME

FreeSurfer::Stats - read FreeSurfer ASEG/APARC statistics files

=head2 METHODS

=over 4

=item read($infile)

Reads a FreeSurfer stats file (ASEG or APARC).  Returns a hash reference
with five entries:

=over 2

=item METADATA

Reference to a name->value hash of metadata in the stats file

=item GLOBALS

Reference to a hash of global measures, mapping from measure name to
a reference to a [value, units] pair.

=item REGIONS

Reference to a list of region results, each item a reference to a hash
mapping data column name to value.

=item UNITS

Reference to a hash mapping data column name to units.

=back

=back

=head1 AUTHOR

FreeSurfer:Stats was written by Kevin A. Archie
E<lt>karchie@npg.wustl.eduE<gt>

=cut

sub read($) {
    my $infile = shift;

    open(STATSFILE, $infile) || die "Can't open $infile: $!";

    # Read the file contents into four categories:
    my %vars;            # metadata
    my @cols;            # data column info (also metadata)
    my %globals;        # global measures
    my @regions;        # region measures
    while (<STATSFILE>) {
        s/\s+\Z//;        # remove trailing whitespace
        if (/\A# Measure\s+(\S.*)\Z/) {
            # global measures
            my ($cat, $name, $desc, $value, $units) = split /,\s+/, $1;
            die "global measure $name multiply defined\n"
            if exists $globals{$name};
            $globals{$name} = [$value, $units];
        } elsif (/\A# TableCol\s+(\S.*)\Z/) {
            # Table column definition
            my $definition = $1;
            if ($definition =~ /(\d+)\s+(\w+)\s+(\S.*)\Z/) {
                my ($index, $name, $desc) = ($1, $2, $3);
                die "Invalid table column definition: $definition\n"
                if !(defined $index && defined $name && defined $desc);
                if (!defined $cols[$index-1]) {
                    $cols[$index-1] = {$name => $desc};
                } else {
                    $cols[$index-1]->{$name} = $desc;
                }
            } else {
                die "Invalid table column definition: $definition\n";
            }
        } elsif (/\A# ColHeaders\s+(\S.*)\Z/) {
            # Use ColHeaders line as a consistency check.
            my @headers = split /\s+/, $1;
            for (my $i = 0; $i <= $#headers; $i++) {
                unless ($headers[$i] eq $cols[$i]->{ColHeader}) {
                    die "Warning: ColHeaders header $headers[$i] ",
                    "inconsistent with TableCol header ",
                    $cols[$i]->{ColHeader},  ".\n";
                }
            }
        } elsif (/\A# (\S+)\s+(\S.*)\Z/) {
            printf "$1 multiply defined\n" if exists $vars{$1};
            $vars{$1} = $2;
        } elsif (/\A#\s*\Z/) {
            # blank line: ignore
        } else {
            # Region data: turn it into a hash keyed from the column headers
            s/\A\s+//;    # remove leading whitespace
            my @vals = split /\s+/;
            my $region = {};
            if ($#vals != $#cols) {
                print STDERR "warning: region line has ", $#vals+1,
                " columns (expected ", $#cols+1, ")\noffending line: $_\n";
            }
            for (my $col = 0; $col <= $#cols; $col++) {
                $region->{$cols[$col]->{ColHeader}} = $vals[$col];
            }
            push @regions, $region;
        }
    }

    close STATSFILE || die "Unable to close $infile: $!";

    # Some variables need to be set up by hand:
    # program_version (derived from CVS Id string)
    if ($vars{cvs_version} =~ /\A\$Id: (\S+) (\d+\.\d+) /) {
        $vars{program_version} = $2;
    } else {
        print STDERR "Unable to read generating program version ",
        "from CVS version information\n";
        $vars{program_version} = 'unknown';
    }
    # timestamp (converted from CreationTime)
    if (exists $vars{CreationTime}
        && $vars{CreationTime} =~ /(\d\d\d\d)\/(\d\d)\/(\d\d)\-(\d\d:\d\d:\d\d)-GMT/) {
        $vars{timestamp} = "$1-$2-$3T$4Z";
        $vars{exptdate} = "$1-$2-$3";
    } else {
        print STDERR "No creation time found in $infile; using dummy timestamp.\n";
        $vars{timestamp} = "0001-01-01T00:00:00Z";
        if (exists $vars{BrainMaskFileTimeStamp}
            && $vars{BrainMaskFileTimeStamp} =~ /(\d\d\d\d)\/(\d\d)\/(\d\d) (\d\d:\d\d:\d\d)/) {
            $vars{exptdate} = "$1-$2-$3";
        }else {
            $vars{exptdate} = undef;
        }
    }

    # cmdargs (converted from cmdline) : command line minus the command
    $vars{cmdline} =~ /\A\S+\s+(\S.*)\Z/;
    $vars{cmdargs} = defined $1 ? $1 : '';

    # Want to be able to access units of table columns.
    my %col_units;
    for my $col (@cols) {
        $col_units{$col->{ColHeader}} = $col->{Units};
    }

    # Do some consistency checks.
    if (exists $vars{NTableCols} && $vars{NTableCols} != $#cols + 1) {
        print STDERR "Warning: NTableCols = $vars{NTableCols}, ",
        "but only ", $#cols + 1, " columns are defined.\n";
    }

    if (exists $vars{NRows} && $vars{NRows} != $#regions + 1) {
        print STDERR "Warning: NRows = $vars{NRows}, ",
        "but only ", $#regions + 1, " rows were read.\n";
    }

    my $resultsref = {};
    $resultsref->{METADATA} = \%vars;
    $resultsref->{UNITS} = \%col_units;
    $resultsref->{GLOBALS} = \%globals;
    $resultsref->{REGIONS} = \@regions;

    return $resultsref;
}

1;
