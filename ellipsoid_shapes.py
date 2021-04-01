# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

ws = CreateMDWorkspace(Dimensions='3', Extents='-2,2,-2,2,-2,2',
                       Names='Q_lab_x,Q_lab_y,Q_lab_z', Units='U,U,U',
                       Frames='QLab,QLab,QLab',
                       SplitInto='2', SplitThreshold='50')
expt_info = CreateSampleWorkspace()
ws.addExperimentInfo(expt_info)

# add peak
p = CreatePeaksWorkspace(InstrumentWorkspace='ws', NumberOfPeaks=0, OutputWorkspace='peaks')
SetUB('peaks', 1,1,1,90,90,90)
pk = p.createPeak([1,1,1]) # axes aligned with viewing axes
p.addPeak(pk)

a=0.3
b=0.4
c=0.5
IntegratePeaksMD(InputWorkspace='ws', PeakRadius=[a,b,c], Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='ellipsoid')

a=0.4
b=0.3
c=0.3
b_in_a = 0.4
b_in_b = 0.4
b_in_c = 0.4
b_out_a = 0.4
b_out_b = 0.5
b_out_c = 0.5
IntegratePeaksMD(InputWorkspace='ws', PeakRadius=[a,b,c], BackgroundInnerRadius=[b_in_a, b_in_b, b_in_c], BackgroundOuterRadius=[b_out_a, b_out_b, b_out_c], Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='ellipsoid_bg')


IntegratePeaksMD(InputWorkspace='ws',
PeakRadius=0.3,
        BackgroundInnerRadius=0.4,
        BackgroundOuterRadius=0.5,
        PeaksWorkspace='peaks', OutputWorkspace='sphere_bg')
