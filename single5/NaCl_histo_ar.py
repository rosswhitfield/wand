from mantid.simpleapi import *

if 'data' in mtd:
    mtd.remove('data')
    
for run in range(2952,4754,1):
    LoadMD(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}_MDE.nxs'.format(run),OutputWorkspace='md')
    BinMD(InputWorkspace='md', OutputWorkspace='mdh', AlignedDim0='Q_sample_x,-10,10,401', AlignedDim1='Q_sample_y,-1,1,41', AlignedDim2='Q_sample_z,-10,10,401')
    if 'data' in mtd:
        PlusMD(LHSWorkspace='data', RHSWorkspace='mdh', OutputWorkspace='data')
    else:
        CloneMDWorkspace(InputWorkspace='mdh', OutputWorkspace='data')
