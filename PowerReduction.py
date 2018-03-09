from mantid.simpleapi import LoadNexus, LoadWAND
from wand import reduceToPowder

name = 'Silicon'
IPTS = 7776
run = 7544
vanadium = 7553 # Run number of `None`
normaliseBy='Monitor' # One on (None, Monitor, Time)
units = 'Theta' # One of (Theta, ElasticQ, ElasticDSpacing)
Binning = '20,140,2500' # Min,Max,Number_of_bins
use_autoreduced = True
use_autoreduced_van = True


###############################################################################

iptsdir = '/HFIR/HB2C/IPTS-{}/'.format(IPTS)

xmin, xmax, bins = Binning.split(',')

if use_autoreduced:        
    ws = LoadNexus(Filename=iptsdir+'shared/autoreduce/HB2C_{}.nxs'.format(run))
else:
    ws = LoadWAND(Filename=iptsdir+'nexus/HB2C_{}.nxs.h5'.format(run))

if vanadium is not None:
    if 'cal' in mtd:
        cal = mtd['cal']
    else:
        if use_autoreduced_van:
            cal = LoadNexus(Filename=iptsdir+'shared/autoreduce/HB2C_{}.nxs'.format(vanadium))
        else:
            cal = LoadWAND(Filename=iptsdir+'shared/autoreduce/HB2C_{}.nxs.h5'.format(vanadium))
else:
    cal = None

reduceToPowder(ws, OutputWorkspace=name, cal=cal, target=units, XMin=xmin, XMax=xmax, NumberBins=bins, normaliseBy=normaliseBy)
