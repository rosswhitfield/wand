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

IntegratePeaksMD(InputWorkspace='ws', PeakRadius=0.5, PeaksWorkspace='peaks', OutputWorkspace='sphere_no_bg')
IntegratePeaksMD(InputWorkspace='ws', PeakRadius=0.5, BackgroundOuterRadius=1.0, PeaksWorkspace='peaks', OutputWorkspace='sphere')
IntegratePeaksMD(InputWorkspace='ws', PeakRadius=[0.5,0.4,0.3], Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='ellipse_no_bg')
IntegratePeaksMD(InputWorkspace='ws', PeakRadius=[0.5,0.5,0.5], BackgroundOuterRadius=[1.0,1.0,1.0], Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='ellipse')
IntegratePeaksMD(InputWorkspace='ws', PeakRadius=[0.5,0.4,0.3], BackgroundInnerRadius=[0.6,0.4,0.5], BackgroundOuterRadius=[1.0,0.4,1.0], Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='ellipse2')
