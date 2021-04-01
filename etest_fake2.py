# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

ws = CreateMDWorkspace(Dimensions='3', Extents='0,2,0,2,0,2',
                       Names='Q_lab_x,Q_lab_y,Q_lab_z', Units='U,U,U',
                       Frames='QLab,QLab,QLab',
                       SplitInto='2', SplitThreshold='50')
expt_info = CreateSampleWorkspace()
ws.addExperimentInfo(expt_info)
nevents=100000000
FakeMDEventData(ws, UniformParams=nevents)

nevents/=8

# add peak
p = CreatePeaksWorkspace(InstrumentWorkspace='ws', NumberOfPeaks=0, OutputWorkspace='peaks')
SetUB('peaks', 1,1,1,90,90,90)
pk = p.createPeak([1,1,1]) # axes aligned with viewing axes
p.addPeak(pk)

r = 1
p=IntegratePeaksMD(InputWorkspace='ws', PeakRadius=r, PeaksWorkspace='peaks', OutputWorkspace='peaks_int')
print(4/3*np.pi*r**3*nevents)
print(p.getPeak(0).getIntensity())

a = 1
b = 1
c = 1
p=IntegratePeaksMD(InputWorkspace='ws', PeakRadius=[a,b,c], Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_int2')
print(4/3*np.pi*a*b*c*nevents)
print(p.getPeak(0).getIntensity())

a = 0.5
b = 0.75
c = 1.0
p=IntegratePeaksMD(InputWorkspace='ws', PeakRadius=[a,b,c], Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_int5')
print(4/3*np.pi*a*b*c*nevents)
print(p.getPeak(0).getIntensity())


r = 0.5
b_i = 0.5001
b = 1.0
p=IntegratePeaksMD(InputWorkspace='ws', PeakRadius=r, BackgroundInnerRadius=b_i, BackgroundOuterRadius=b, PeaksWorkspace='peaks', OutputWorkspace='peaks_int')
print(p.getPeak(0).getIntensity())


a = 0.5
b = 0.5
c = 0.5
a_back = 1.0
b_back = 0.6
c_back = 1.0
p=IntegratePeaksMD(InputWorkspace='ws', PeakRadius=[a,b,c], BackgroundOuterRadius=[a_back, b_back, c_back], Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_int4')
print(p.getPeak(0).getIntensity())
