import numpy as np
from mantid.simpleapi import *

van = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_1035.nxs.h5')
van = Integration(van)
MaskDetectors(van,DetectorList=range(16384))
van.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(van.getNumberHistograms()):
    van.setX(idx, w)
van=ConvertToEventWorkspace(van)
SetGoniometer('van', Axis0="HB2C:Mot:s1,0,1,0,1")

"""
ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_1078.nxs.h5')
ws = Integration(ws)
MaskDetectors(ws,DetectorList=range(16384))

ws.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(ws.getNumberHistograms()):
    ws.setX(idx, w)
ws=ConvertToEventWorkspace(ws)
SetGoniometer(ws, Axis0="HB2C:Mot:s1,0,1,0,1")
SetGoniometer(ws, Axis0="HB2C:Mot:s1,0,1,0,1")
ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md')
"""

# Do multiple

if 'mdh' in mtd:
    mtd.remove('md')
    
if 'van_mdh' in mtd:
    mtd.remove('van_md')

for run in range(1834,2871,1):
    if run == 1796:
        continue
    ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_{}.nxs.h5'.format(run))
    ws = Integration(ws)
    MaskDetectors(ws,DetectorList=range(16384))
    ws.getAxis(0).setUnit("Wavelength")
    for idx in xrange(ws.getNumberHistograms()):
        ws.setX(idx, w)
    ws=ConvertToEventWorkspace(ws)
    SetGoniometer('ws', Axis0="HB2C:Mot:s1,0,1,0,1")
    ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md',MinValues='-10,-10,-10',MaxValues='10,10,10')
    # Van, copy goniometer
    mtd['van'].run().getGoniometer().setR(mtd['ws'].run().getGoniometer().getR())
    ConvertToMD('van', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='van_md',MinValues='-10,-10,-10',MaxValues='10,10,10')
    mdh_tmp = BinMD(InputWorkspace='md', AlignedDim0='Q_sample_x,-10,10,401', AlignedDim1='Q_sample_y,-1,1,41', AlignedDim2='Q_sample_z,-10,10,401')
    van_mdh_tmp = BinMD(InputWorkspace='van_md', AlignedDim0='Q_sample_x,-10,10,401', AlignedDim1='Q_sample_y,-1,1,41', AlignedDim2='Q_sample_z,-10,10,401')
    if 'mdh' in mtd:
        mdh = mdh + mdh_tmp
    else:
        mdh=CloneWorkspace(mdh_tmp)
    if 'van_mdh' in mtd:
        van_mdh = van_mdh + van_mdh_tmp
    else:
        van_mdh=CloneWorkspace(van_mdh_tmp)
    if run%20 == 0:
        norm = mdh/van_mdh
        SaveMD('mdh', '/SNS/users/rwp/wand/Ho2PdSi3_data_MDH2_short.nxs')
        SaveMD('van_mdh', '/SNS/users/rwp/wand/Ho2PdSi3_van_MDH2_short.nxs')
        SaveMD('norm', '/SNS/users/rwp/wand/Ho2PdSi3_norm_MDH2_short.nxs')

norm = mdh/van_mdh
SaveMD('mdh', '/SNS/users/rwp/wand/Ho2PdSi3_data_MDH2_short.nxs')
SaveMD('van_mdh', '/SNS/users/rwp/wand/Ho2PdSi3_van_MDH2_short.nxs')
SaveMD('norm', '/SNS/users/rwp/wand/Ho2PdSi3_norm_MDH2_short.nxs')


# md=LoadMD('/SNS/users/rwp/wand/Ho2PdSi3_data_MDE.nxs', LoadHistory=False)
# van_md=LoadMD('/SNS/users/rwp/wand/Ho2PdSi3_van_MDE.nxs', LoadHistory=False)
# mdh=LoadMD('/SNS/users/rwp/wand/Ho2PdSi3_data_MDH.nxs', LoadHistory=False)
# van_mdh=LoadMD('/SNS/users/rwp/wand/Ho2PdSi3_van_MDH.nxs', LoadHistory=False)
# norm=LoadMD('/SNS/users/rwp/wand/Ho2PdSi3_norm_MDH.nxs', LoadHistory=False)
