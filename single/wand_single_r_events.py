import sys
import numpy as np
from mantid.simpleapi import *

van = LoadNexus(Filename='/SNS/users/rwp/wand/HB2C_1035_van.nxs')

start = int(sys.argv[1])
end = int(sys.argv[2])

for run in range(start,end+1):
    ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_{}.nxs.h5'.format(run))
    ws = Integration(ws)
    MaskDetectors(ws, MaskedWorkspace='van')
    ws.getAxis(0).setUnit("Wavelength")
    w = np.array([1.487,1.489])
    for idx in xrange(ws.getNumberHistograms()):
        ws.setX(idx, w)
    ws=ConvertToEventWorkspace(ws)
    SetGoniometer('ws', Axis0="HB2C:Mot:s1,0,1,0,1")
    ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md',MinValues='-10,-1,-10',MaxValues='10,1,10')
    # Van, copy goniometer
    mtd['van'].run().getGoniometer().setR(mtd['ws'].run().getGoniometer().getR())
    ConvertToMD('van', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='van_md',MinValues='-10,-1,-10',MaxValues='10,1,10')
    SaveMD('md', '/SNS/users/rwp/wand/MDE/Ho2PdSi3_{}_data_MDE.nxs'.format(run))
    SaveMD('van_md', '/SNS/users/rwp/wand/MDE/Ho2PdSi3_{}_van_MDE.nxs'.format(run))
