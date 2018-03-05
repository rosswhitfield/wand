from wand import accumulateMD
from mantid.simpleapi import (LoadMD, DeleteWorkspace, LoadWAND,
                              SaveMD, BinMD, ConvertToMD, mtd)

# change to following values

name = 'PNO'
append = False
IPTS = 7776
first_run = 4756
last_run = 6557
load_every = 100
use_autoreduced = True

# Binning for MD histo workspace; min,max,number_of_bins
BinningDim0 = '-10,10,1000'
BinningDim1 = '-1,1,100'
BinningDim2 = '-10,10,1000'

# After running this you should find peaks and UB matrix

###############################################################################
#                    Do not edit below                                        #
###############################################################################

# Load data and accumulate to Q sample MD event workspace

iptsdir = '/HFIR/HB2C/IPTS-{}/'.format(IPTS)

name_MDE = name+'_MDE'
filename = ''

if not append and name_MDE in mtd:
    DeleteWorkspace(name_MDE)

try:
    for run in range(first_run, last_run+1, load_every):
        if use_autoreduced:
            filename = iptsdir+'shared/autoreduce/HB2C_{}_MDE.nxs'.format(run)
            LoadMD(Filename=filename, LoadHistory=False,
                   OutputWorkspace='__md')
        else:
            filename = iptsdir+'nexus/HB2C_{}.nxs.h5'.format(run)
            LoadWAND(filename, OutputWorkspace='__ws')
            ConvertToMD('__ws', QDimensions='Q3D', dEAnalysisMode='Elastic',
                        Q3DFrames='Q_sample', OutputWorkspace='__md',
                        MinValues='-10,-1,-10', MaxValues='10,1,10')
        accumulateMD('__md', OutputWorkspace=name_MDE)
except ValueError:
    print("Could not load run {}\nSaving anyway".format(run))
    SaveMD(name_MDE,
           iptsdir+'shared/'+name+'_MDE_{}_to_{}_every_{}.nxs'.format(first_run,
                                                                      run,
                                                                      load_every))
    raise ValueError("Could not load run {}".format(run))

SaveMD(name_MDE,
       iptsdir+'shared/'+name+'_MDE_{}_to_{}_every_{}.nxs'.format(first_run,
                                                                  last_run,
                                                                  load_every))

# Convert MD Event workspace to MD Histo workspace

name_MDH = name+'_MDH'

BinMD(InputWorkspace=name_MDE,
      AlignedDim0='Q_sample_x,'+BinningDim0,
      AlignedDim1='Q_sample_y,'+BinningDim1,
      AlignedDim2='Q_sample_z,'+BinningDim2,
      OutputWorkspace=name_MDH)

SaveMD(name_MDH,
       iptsdir+'shared/'+name+'_MDH_{}_to_{}_every_{}.nxs'.format(first_run,
                                                                  last_run,
                                                                  load_every))

