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

if 'md' in mtd:
    mtd.remove('md')
    
if 'van_md' in mtd:
    mtd.remove('van_md')

for run in range(1059,1834,1):
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
    ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md',OverwriteExisting=False,MinValues='-10,-10,-10',MaxValues='10,10,10')
    # Van, copy goniometer
    mtd['van'].run().getGoniometer().setR(mtd['ws'].run().getGoniometer().getR())
    ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='van_md',OverwriteExisting=False,MinValues='-10,-10,-10',MaxValues='10,10,10')
    if run%20 == 0:
        SaveMD('md', '/SNS/users/rwp/wand/Ho2PdSi3_data_MDE.nxs')
        SaveMD('van_md', '/SNS/users/rwp/wand/Ho2PdSi3_van_MDE.nxs')

SaveMD('md', '/SNS/users/rwp/wand/Ho2PdSi3_data_MDE.nxs')
SaveMD('van_md', '/SNS/users/rwp/wand/Ho2PdSi3_van_MDE.nxs')


# md=LoadMD('/SNS/users/rwp/wand/Ho2PdSi3_data_MDE.nxs')
# van_md=LoadMD('/SNS/users/rwp/wand/Ho2PdSi3_van_MDE.nxs')

