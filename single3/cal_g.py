import numpy as np
from mantid.simpleapi import *

w = np.array([1.487,1.489])


ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_2972.nxs.h5')
ws = Integration(ws)
MaskDetectors(ws,DetectorList=range(16384))
ws.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(ws.getNumberHistograms()):
    ws.setX(idx, w)
SetGoniometer(ws, Axis0="HB2C:Mot:s1,0,1,0,1")
print(ws.run().getGoniometer().getR())

ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md_sample')
ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_lab', OutputWorkspace='md_lab')

FindPeaksMD(InputWorkspace='md_sample', PeakDistanceThreshold=0.5, DensityThresholdFactor=500, OutputWorkspace='peaks')
FindPeaksMD(InputWorkspace='md_lab', PeakDistanceThreshold=0.5, DensityThresholdFactor=500, OutputWorkspace='peaks_lab')

p0=mtd['peaks'].getPeak(0)
print(p0.getQSampleFrame())
print(p0.getQLabFrame())
print(p0.getWavelength())
print(p0.getGoniometerMatrix())
