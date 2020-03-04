#!/usr/bin/env python

def generateBidsNameMap(bidsFileName):
    """ 
    The BIDS file names will look like
    sub-<participant_label>[_ses-<session_label>][_acq-<label>][_ce-<label>][_rec-<label>][_run-<index>][_mod-<label>]_<modality_label>
    (that example is for anat. There may be other fields and labels in the other file types.)
    So we split by underscores to get the individual field values.
    However, some of the values may contain underscores themselves, so we have to check that each entry (save the last)
      contains a -.
    """
    underscoreSplitListRaw = bidsFileName.split('_')
    underscoreSplitList = []

    for splitListEntryRaw in underscoreSplitListRaw[:-1]:
        if '-' not in splitListEntryRaw:
            underscoreSplitList[-1] = underscoreSplitList[-1] + splitListEntryRaw
        else:
            underscoreSplitList.append(splitListEntryRaw)

    bidsNameMap = dict(splitListEntry.split('-') for splitListEntry in underscoreSplitList)
    bidsNameMap['modality'] = underscoreSplitListRaw[-1]

    return bidsNameMap

def getSubdir(modality):
    """
    Return the BIDS subdir based on modality (will be downcased for you)
    """
    bidsAnatModalities = ['t1w', 't2w', 't1rho', 't1map', 't2map', 't2star', 'flair', 'flash', 'pd', 'pdmap', 'pdt2', 'inplanet1', 'inplanet2', 'angio', 'defacemask', 'swimagandphase']
    bidsFuncModalities = ['bold', 'physio', 'stim', 'sbref']
    bidsDwiModalities = ['dwi', 'dti']
    bidsBehavioralModalities = ['beh']
    bidsFieldmapModalities = ['phasemap', 'magnitude1', 'epi']

    modalityLowercase = modality.lower()
    return 'anat' if modalityLowercase in bidsAnatModalities else \
           'func' if modalityLowercase in bidsFuncModalities else \
           'dwi' if modalityLowercase in bidsDwiModalities else \
           'beh' if modalityLowercase in bidsBehavioralModalities else \
           'fmap' if modalityLowercase in bidsFieldmapModalities else \
           None

