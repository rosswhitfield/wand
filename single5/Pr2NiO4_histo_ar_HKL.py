from mantid.simpleapi import *
from mantid.geometry import OrientedLattice

van=LoadNexus('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}.nxs'.format(6558))
LoadIsawUB('van','/SNS/users/rwp/wand/single5/PNO.mat')
ub=mtd['van'].sample().getOrientedLattice().getUB().copy()

ol = OrientedLattice()
ol.setUB(ub)
q1 = ol.qFromHKL([1, 0, 0])
q2 = ol.qFromHKL([0, 1, 0])
q3 = ol.qFromHKL([0, 0, 1])        

if 'data' in mtd:
    mtd.remove('data')
    
if 'norm' in mtd:
    mtd.remove('norm')
    
for run in range(4756,6558,1):
    print(run)
    md=LoadMD(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}_MDE.nxs'.format(run))
    mtd['van'].run().getGoniometer().setR(mtd['md'].getExperimentInfo(0).run().getGoniometer().getR())
    
    #BinMD(InputWorkspace='md', OutputWorkspace='mdh', AlignedDim0='Q_sample_x,-10,10,401', AlignedDim1='Q_sample_y,-1,1,41', AlignedDim2='Q_sample_z,-10,10,401')
    BinMD(InputWorkspace='md',OutputWorkspace='mdh', AxisAligned=False,
          BasisVector0='[H,0,0],A^-1,{},{},{}'.format(q1.X(), q1.Y(), q1.Z()),
          BasisVector1='[0,K,0],A^-1,{},{},{}'.format(q2.X(), q2.Y(), q2.Z()),
          BasisVector2='[0,0,L],A^-1,{},{},{}'.format(q3.X(), q3.Y(), q3.Z()),
          OutputExtents='-8,8,-8,8,-1.5,2.5', OutputBins='401,401,101')
    
    ConvertToMD('van', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='HKL', OutputWorkspace='van_md',MinValues='-10,-10,-10',MaxValues='10,10,10')
    BinMD(InputWorkspace='van_md', OutputWorkspace='van_mdh',  AlignedDim0='[H,0,0],-8,8,401', AlignedDim1='[0,K,0],-8,8,401', AlignedDim2='[0,0,L],-1.5,2.5,101')
    if 'data' in mtd:
        PlusMD(LHSWorkspace='data', RHSWorkspace='mdh', OutputWorkspace='data')
        PlusMD(LHSWorkspace='norm', RHSWorkspace='van_mdh', OutputWorkspace='norm')
    else:
        CloneMDWorkspace(InputWorkspace='mdh', OutputWorkspace='data')
        CloneMDWorkspace(InputWorkspace='van_mdh', OutputWorkspace='norm')
    if run%100 == 0:
        SaveMD('data', '/HFIR/HB2C/IPTS-7776/shared/rwp/PNO_data_MDH_HKL.nxs')
        SaveMD('norm', '/HFIR/HB2C/IPTS-7776/shared/rwp/PNO_van_MDH_HKL.nxs')
        norm_data = DivideMD('data','norm')

SaveMD('data', '/HFIR/HB2C/IPTS-7776/shared/rwp/PNO_data_MDH_HKL.nxs')
SaveMD('norm', '/HFIR/HB2C/IPTS-7776/shared/rwp/PNO_van_MDH_HKL.nxs')

norm_data = DivideMD('data','norm')
