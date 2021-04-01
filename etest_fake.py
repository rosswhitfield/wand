# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

ws = CreateMDWorkspace(Dimensions='3', Extents='0.5,1.5,0.5,1.5,0.5,1.5',
                       Names='Q_lab_x,Q_lab_y,Q_lab_z', Units='U,U,U',
                       Frames='QLab,QLab,QLab',
                       SplitInto='2', SplitThreshold='50')
expt_info = CreateSampleWorkspace()
ws.addExperimentInfo(expt_info)
nevents=100000000
FakeMDEventData(ws, UniformParams=nevents)

# add peak
p = CreatePeaksWorkspace(InstrumentWorkspace='ws', NumberOfPeaks=0, OutputWorkspace='peaks')
SetUB('peaks', 1,1,1,90,90,90)
pk = p.createPeak([1,1,1]) # axes aligned with viewing axes
p.addPeak(pk)

"""
r = 0.3
back = 0.5
p=IntegratePeaksMD(InputWorkspace='ws', PeakRadius=r, PeaksWorkspace='peaks', OutputWorkspace='peaks_int3', BackgroundOuterRadius=back)
print(4/3*np.pi*r**3*nevents - 4/3*np.pi*(back**3 - r**3)*nevents*r**3/(back**3 - r**3))
print(p.getPeak(0).getIntensity())
print(4/3*np.pi*(back**3 - r**3)*nevents)

a = 0.3
b = 0.3
c = 0.3
a_back = 0.5
b_back = 0.5
c_back = 0.5
p=IntegratePeaksMD(InputWorkspace='ws', PeakRadius=[a,b,c], BackgroundOuterRadius=[a_back, b_back, c_back], Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_int4')
print(4/3*np.pi*a*b*c*nevents - 4/3*np.pi*(a_back*b_back*c_back - a*b*c)*nevents*a*b*c/(a_back*b_back*c_back - a*b*c))
print(p.getPeak(0).getIntensity())
print(4/3*np.pi*(a_back*b_back*c_back - a*b*c)*nevents)
"""

a = 0.005
b = 0.013
c = 0.013
p=IntegratePeaksMD(InputWorkspace='ws', PeakRadius=[a,b,c], Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='ellipse2')
print(p.getPeak(0).getIntensity())
print(4/3*np.pi*(a*b*c)*nevents)


r=0.013
a=0.013
b=0.013
c=0.013
IntegratePeaksMD(InputWorkspace='ws', PeakRadius=r, PeaksWorkspace='peaks', OutputWorkspace='peaks_sphere')
IntegratePeaksMD(InputWorkspace='ws', PeakRadius=[a,b,c], Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_ellipse')
