# The following line helps with future compatibility with Python 3
# print must now be used as a function, e.g print('Hello','World')
from __future__ import (absolute_import, division, print_function, unicode_literals)

# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *

import matplotlib.pyplot as plt

import numpy as np

data = LoadWANDSCD(IPTS=22745, RunNumbers='147131-148931', Grouping='4x4')
mde=ConvertSCDtoMDE(data, wavelength=1.488,MinValues='-10,-10,-10',MaxValues='10,10,10')

PredictPeaks(InputWorkspace=data,
MinDSpacing=0.5,
ReflectionCondition='Rhombohedrally centred, obverse',
             CalculateGoniometerForCW=True,
             Wavelength=1.488, MinAngle=-90,MaxAngle=90,
             CalculateStructureFactors=True,
             OutputWorkspace='predict')

IntegratePeaksMD(InputWorkspace=mde, PeaksWorkspace='predict', PeakRadius=0.5, OutputWorkspace='integrated')

peaks = mtd["integrated"]
for p in range(peaks.getNumberPeaks()):
        peak = peaks.getPeak(p)
        lorentz = np.sin(2*np.arcsin(1.488/(2*peak.getDSpacing())))
        print("HKL = {:>12} int = {:>8} {:5.1f}".format(str(peak.getHKL()),peak.getIntensity(),peak.getIntensity()*lorentz))
