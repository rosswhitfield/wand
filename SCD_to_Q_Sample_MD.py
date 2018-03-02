from wand import convertToQSample, convertQSampleToHKL, accumulateMD
from mantid.simpleapi import LoadNexus, LoadMD, DeleteWorkspace, DivideMD


# change to following values

name = 'PNO'
IPTS = 7776
first_run = 4756
last_run = 6557
load_every = 4




################################################################################
#                    Do not edit below                                         #
################################################################################


### Load autoreduced data and acculate to Q sample MD event workspace

shareddir='/HFIR/HB2C/IPTS-{}/shared/'.format(IPTS)

if name in mtd:
    DeleteWorkspace(name)

for filename in [shareddir+'autoreduce/HB2C_{}_MDE.nxs'.format(run) for run in range(first_run,last_run,load_every)]:
                 LoadMD(Filename=filename, LoadHistory=False, OutputWorkspace='__md')
                 accumulateMD('__md', OutputWorkspace=name)
                 
SaveMD(name, shareddr+name+'_MDE_{}_to{}_every{}.nxs'.format(first_run,last_run,load_every))


### Convert MD Event workspace to MD Histo workspace

BinMD(InputWorkspace='data', AlignedDim0='Q_sample_x,-10,10,1000', AlignedDim1='Q_sample_y,-1,1,50', AlignedDim2='Q_sample_z,0,10,500', OutputWorkspace='mdh')
