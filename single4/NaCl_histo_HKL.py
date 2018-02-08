import numpy as np
from mantid.simpleapi import *

van=LoadNexus('/SNS/users/rwp/wand/HB2C_2933_Van_processed.nxs')

#NaCl 2952 - 4753

if 'data' in mtd:
    mtd.remove('data')
    
if 'norm' in mtd:
    mtd.remove('norm')

for run in range(2952,4754,1):
    ws=LoadNexus(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}.nxs'.format(run))
    SetGoniometer('ws', Axis0="HB2C:Mot:s1,0,1,0,1")
    LoadIsawUB('ws','/SNS/users/rwp/wand/single4/nacl.mat')
    LoadIsawUB('van','/SNS/users/rwp/wand/single4/nacl.mat')
    ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='HKL', QConversionScales='HKL', OutputWorkspace='md',MinValues='-10,-10,-10',MaxValues='10,10,10')
    # Van, copy goniometer
    mtd['van'].run().getGoniometer().setR(mtd['ws'].run().getGoniometer().getR())
    ConvertToMD('van', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='HKL', QConversionScales='HKL', OutputWorkspace='van_md',MinValues='-10,-10,-10',MaxValues='10,10,10')
    BinMD(InputWorkspace='md', OutputWorkspace='mdh',  AlignedDim0='[H,0,0],-10,10,401', AlignedDim1='[0,K,0],-10,10,401', AlignedDim2='[0,0,L],-10,10,401')
    BinMD(InputWorkspace='van_md', OutputWorkspace='van_mdh',  AlignedDim0='[H,0,0],-10,10,401', AlignedDim1='[0,K,0],-10,10,401', AlignedDim2='[0,0,L],-10,10,401')
    if 'data' in mtd:
        PlusMD(LHSWorkspace='data', RHSWorkspace='mdh', OutputWorkspace='data')
        PlusMD(LHSWorkspace='norm', RHSWorkspace='van_mdh', OutputWorkspace='norm')
    else:
        CloneMDWorkspace(InputWorkspace='mdh', OutputWorkspace='data')
        CloneMDWorkspace(InputWorkspace='van_mdh', OutputWorkspace='norm')
    if run%200 == 0:
        SaveMD('data', '/HFIR/HB2C/IPTS-7776/shared/rwp/NaCl_data_MDH_HKL.nxs')
        SaveMD('norm', '/HFIR/HB2C/IPTS-7776/shared/rwp/NaCl_van_MDH_HKL.nxs')

SaveMD('data', '/HFIR/HB2C/IPTS-7776/shared/rwp/NaCl_data_MDH_HKL.nxs')
SaveMD('norm', '/HFIR/HB2C/IPTS-7776/shared/rwp/NaCl_van_MDH_HKL.nxs')
