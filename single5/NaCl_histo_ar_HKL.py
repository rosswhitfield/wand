from mantid.simpleapi import *

CreateSingleValuedWorkspace(OutputWorkspace='ub')
LoadIsawUB('ub','/SNS/users/rwp/wand/single4/nacl.mat')
ub=mtd['ub'].sample().getOrientedLattice().getUB().copy()

if 'data' in mtd:
    mtd.remove('data')
    
for run in range(2952,4754,1):
    LoadMD(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}_MDE.nxs'.format(run),OutputWorkspace='md')
    ConvertCWSDMDtoHKL('md', UBMatrix=ub, OutputWorkspace='md2')
    BinMD(InputWorkspace='md2', OutputWorkspace='mdh', AlignedDim0='H,-0.5,0.5,41', AlignedDim1='K,-10,10,401', AlignedDim2='L,-10,10,401')
    if 'data' in mtd:
        PlusMD(LHSWorkspace='data', RHSWorkspace='mdh', OutputWorkspace='data')
    else:
        CloneMDWorkspace(InputWorkspace='mdh', OutputWorkspace='data')
