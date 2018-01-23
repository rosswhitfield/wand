import numpy as np
from mantid.simpleapi import *

w = np.array([1.487,1.489])

#data=LoadMD('/HFIR/HB2C/IPTS-7776/shared/rwp/NaCl_data_MDH3.nxs', LoadHistory=False)

run = 4753

LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_{}.nxs.h5'.format(run),OutputWorkspace='ws')
LoadInstrument(Workspace='ws',Filename='/SNS/users/rwp/wand/single3/WAND_Definition2.xml')
Integration(InputWorkspace='ws',OutputWorkspace='ws')
MaskDetectors('ws',DetectorList=range(16384))
#GroupDetectors(InputWorkspace='ws',OutputWorkspace='ws',CopyGroupingFromWorkspace='van')
mtd['ws'].getAxis(0).setUnit("Wavelength")
for idx in xrange(mtd['ws'].getNumberHistograms()):
    mtd['ws'].setX(idx, w)
SetGoniometer('ws', Axis0="HB2C:Mot:s1,0,1,0,1")
ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md',MinValues='-10,-10,-10',MaxValues='10,10,10')
BinMD(InputWorkspace='md', OutputWorkspace='mdh', AlignedDim0='Q_sample_x,-10,10,401', AlignedDim1='Q_sample_y,-1,1,41', AlignedDim2='Q_sample_z,-10,10,401')
PlusMD(LHSWorkspace='mdh', RHSWorkspace='data', OutputWorkspace='data2')
