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
nevents=10000000
FakeMDEventData(ws, UniformParams=f'{nevents},0.98,1.02,0.98,1.02,0.98,1.02')
# add peak
p = CreatePeaksWorkspace(InstrumentWorkspace='ws', NumberOfPeaks=0, OutputWorkspace='peaks')
SetUB('peaks', 1,1,1,90,90,90)
pk = p.createPeak([1,1,1]) # axes aligned with viewing axes
p.addPeak(pk)
a = 0.005
b = 0.013
c = 0.013
#a=b=c=0.005
p=IntegratePeaksMD(InputWorkspace='ws', PeakRadius=[a,b,c], Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='ellipsoid')
print("Integrate Intensity =", p.getPeak(0).getIntensity())
print("Approx. Expected Intensity=", 4/3*np.pi*(a*b*c)*nevents*25**3)
