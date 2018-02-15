from mantid.simpleapi import *
from mantid.geometry import OrientedLattice

van=LoadNexus('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}.nxs'.format(6558))
LoadIsawUB('van','/SNS/users/rwp/wand/single5/PNO.mat')

if 'data' in mtd:
    mtd.remove('data')
    
if 'norm' in mtd:
    mtd.remove('norm')
    
for run in range(4756,6558,1):
    print(run)
    ws=LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_{}.nxs.h5'.format(run))
    mtd['van'].run().getGoniometer().setR(ws.run().getGoniometer().getR())
    LoadIsawUB(ws,'/SNS/users/rwp/wand/single5/PNO.mat')
    ws = Integration(ws)
    MaskDetectors(ws,DetectorList=range(16384))
    ws.getAxis(0).setUnit("Wavelength")
    w = np.array([1.487,1.489])
    for idx in xrange(ws.getNumberHistograms()):
        ws.setX(idx, w)
    SetGoniometer('ws', Axis0="HB2C:Mot:s1,0,1,0,1")            
    ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='HKL', QConversionScales='HKL', OutputWorkspace='md',MinValues='-10,-10,-10',MaxValues='10,10,10')
    ConvertToMD('van', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='HKL', QConversionScales='HKL', OutputWorkspace='van_md',MinValues='-10,-10,-10',MaxValues='10,10,10')
    BinMD(InputWorkspace='md', OutputWorkspace='mdh',  AlignedDim0='[H,0,0],-8,8,401', AlignedDim1='[0,K,0],-8,8,401', AlignedDim2='[0,0,L],-1.5,2.5,101')
    BinMD(InputWorkspace='van_md', OutputWorkspace='van_mdh',  AlignedDim0='[H,0,0],-8,8,401', AlignedDim1='[0,K,0],-8,8,401', AlignedDim2='[0,0,L],-1.5,2.5,101')
    if 'data' in mtd:
        PlusMD(LHSWorkspace='data', RHSWorkspace='mdh', OutputWorkspace='data')
        PlusMD(LHSWorkspace='norm', RHSWorkspace='van_mdh', OutputWorkspace='norm')
    else:
        CloneMDWorkspace(InputWorkspace='mdh', OutputWorkspace='data')
        CloneMDWorkspace(InputWorkspace='van_mdh', OutputWorkspace='norm')
    if run%100 == 0:
        SaveMD('data', '/HFIR/HB2C/IPTS-7776/shared/rwp/PNO_data_MDH_HKL_nAR.nxs')
        SaveMD('norm', '/HFIR/HB2C/IPTS-7776/shared/rwp/PNO_van_MDH_HKL_nAR.nxs')
        norm_data = DivideMD('data','norm')

SaveMD('data', '/HFIR/HB2C/IPTS-7776/shared/rwp/PNO_data_MDH_HKL_nAR.nxs')
SaveMD('norm', '/HFIR/HB2C/IPTS-7776/shared/rwp/PNO_van_MDH_HKL_nAR.nxs')

norm_data = DivideMD('data','norm')
