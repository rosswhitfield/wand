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
nevents = 10000000
FakeMDEventData(ws, UniformParams=nevents)


# add peak
p = CreatePeaksWorkspace(InstrumentWorkspace='ws',
                         NumberOfPeaks=0, OutputWorkspace='peaks')
SetUB('peaks', 1, 1, 1, 90, 90, 90)
pk = p.createPeak([1, 1, 1])  # axes aligned with viewing axes
p.addPeak(pk)

a = 0.4
b = 0.3
c = 0.2
a_back = 0.4
b_back = 0.45
c_back = 0.5
p = IntegratePeaksMD(InputWorkspace='ws', PeakRadius=[a, b, c], BackgroundOuterRadius=[
                     a_back, b_back, c_back], Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_int')
print(4/3*np.pi*(a_back*b_back*c_back - a*b*c)*nevents)
print(p.getPeak(0).getPeakShape().toJSON())
