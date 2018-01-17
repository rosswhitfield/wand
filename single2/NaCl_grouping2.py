import numpy as np
from mantid.simpleapi import *

w = np.array([1.487,1.489])

"""
van = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_2933.nxs.h5')
van = Integration(van)
MaskDetectors(van,DetectorList=range(16384))
van=GroupDetectors(van, MapFile='/SNS/users/rwp/wand/single2/HB2C_4x4.map')
van.getAxis(0).setUnit("Wavelength")
for idx in xrange(van.getNumberHistograms()):
    van.setX(idx, w)
SetGoniometer('van', Axis0="HB2C:Mot:s1,0,1,0,1")
SaveNexus('van','/SNS/users/rwp/wand/HB2C_2933_Van_processed_grouped.nxs')
"""
van=LoadNexus('/SNS/users/rwp/wand/HB2C_2933_Van_processed_grouped.nxs')

#NaCl 2952 - 4753
"""
ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_2952.nxs.h5')
ws = Integration(ws)
MaskDetectors(ws,DetectorList=range(16384))
ws=GroupDetectors(ws,CopyGroupingFromWorkspace='van')
ws.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(ws.getNumberHistograms()):
    ws.setX(idx, w)
SetGoniometer(ws, Axis0="HB2C:Mot:s1,0,1,0,1")

ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md')
"""
# Do multiple

if 'data' in mtd:
    mtd.remove('data')
    
if 'norm' in mtd:
    mtd.remove('norm')

for run in range(2952,4754,1):
    ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_{}.nxs.h5'.format(run))
    ws = Integration(ws)
    MaskDetectors(ws,DetectorList=range(16384))
    ws=GroupDetectors(ws,CopyGroupingFromWorkspace='van')
    ws.getAxis(0).setUnit("Wavelength")
    for idx in xrange(ws.getNumberHistograms()):
        ws.setX(idx, w)
    SetGoniometer('ws', Axis0="HB2C:Mot:s1,0,1,0,1")
    ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md',MinValues='-10,-10,-10',MaxValues='10,10,10')
    # Van, copy goniometer
    mtd['van'].run().getGoniometer().setR(mtd['ws'].run().getGoniometer().getR())
    ConvertToMD('van', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='van_md',MinValues='-10,-10,-10',MaxValues='10,10,10')
    if 'data' in mtd:
        mtd['data'] = mtd['data'] + mtd['md']
        mtd['norm'] = mtd['norm'] + mtd['van_md']
    else:
        data=CloneMDWorkspace('md')
        norm=CloneMDWorkspace('van_md')
    if run%100 == 0:
        SaveMD('data', '/SNS/users/rwp/wand/NaCl_data_MDE.nxs')
        SaveMD('norm', '/SNS/users/rwp/wand/NaCl_van_MDE.nxs')

SaveMD('data', '/SNS/users/rwp/wand/NaCl_data_MDE.nxs')
SaveMD('norm', '/SNS/users/rwp/wand/NaCl_van_MDE.nxs')

"""
data=LoadMD('/SNS/users/rwp/wand/NaCl_data_MDE.nxs', LoadHistory=False)
norm=LoadMD('/SNS/users/rwp/wand/NaCl_van_MDE.nxs', LoadHistory=False)
"""

mdh = BinMD(InputWorkspace='data', AlignedDim0='Q_sample_x,-10,10,401', AlignedDim1='Q_sample_y,-1,1,41', AlignedDim2='Q_sample_z,-10,10,401')
van_mdh = BinMD(InputWorkspace='norm', AlignedDim0='Q_sample_x,-10,10,401', AlignedDim1='Q_sample_y,-1,1,41', AlignedDim2='Q_sample_z,-10,10,401')
norm_mdh = mdh/van_mdh

FindPeaksMD(InputWorkspace='mdh', PeakDistanceThreshold=0.5, MaxPeaks=10, DensityThresholdFactor=10000, OutputWorkspace='peaks')
