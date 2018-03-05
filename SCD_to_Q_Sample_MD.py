from wand import convertToQSample, convertQSampleToHKL, accumulateMD
from mantid.simpleapi import LoadNexus, LoadMD, DeleteWorkspace, DivideMD

# change to following values

name = 'PNO'
append = False
IPTS = 7776
first_run = 4756
last_run = 6557
load_every = 50
use_autoreduced = True

# For MD histo workspace
BinningDim0 = '-10,10,1000'
BinningDim1 = '-1,1,100'
BinningDim2 = '-10,10,1000'

# After running this you should find peaks and UB matrix

################################################################################
#                    Do not edit below                                         #
################################################################################


### Load autoreduced data and acculate to Q sample MD event workspace

shareddir='/HFIR/HB2C/IPTS-{}/shared/'.format(IPTS)

name_MDE = name+'_MDE'

if not append and name_MDE in mtd:
    DeleteWorkspace(name_MDE)

try:
    for run in range(first_run,last_run+1,load_every):
        filename=shareddir+'autoreduce/HB2C_{}_MDE.nxs'.format(run)
        LoadMD(Filename=filename, LoadHistory=False, OutputWorkspace='__md')
        accumulateMD('__md', OutputWorkspace=name_MDE)
except:
    print("Could not load run {}\nSaving anyway".format(run))
    SaveMD(name_MDE, shareddr+name+'_MDE_{}_to{}_every{}.nxs'.format(first_run,run,load_every))
    raise ValueError("Could not load run {}".format(run)
    
SaveMD(name_MDE, shareddr+name+'_MDE_{}_to{}_every{}.nxs'.format(first_run,last_run,load_every))

### Convert MD Event workspace to MD Histo workspace

name_MDH = name+'_MDH'

BinMD(InputWorkspace=name_MDE, AlignedDim0='Q_sample_x,-10,10,1000', AlignedDim1='Q_sample_y,-1,1,50', AlignedDim2='Q_sample_z,0,10,500', OutputWorkspace=name_MDH)

