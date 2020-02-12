# The following line helps with future compatibility with Python 3
# print must now be used as a function, e.g print('Hello','World')
from __future__ import (absolute_import, division, print_function, unicode_literals)

# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *

import matplotlib.pyplot as plt

import numpy as np

data = LoadWANDSCD(IPTS=22745, RunNumbers='145330-147130')
mde = ConvertHFIRSCDtoMDE(data, wavelength=1.488)

PredictPeaks(InputWorkspace=data,
             MinDSpacing=0.5,
             ReflectionCondition='Rhombohedrally centred, obverse',
             CalculateGoniometerForCW=True,
             Wavelength=1.488,
             MinAngle=-90,MaxAngle=90,
             CalculateStructureFactors=True,
             OutputWorkspace='predict')

IntegratePeaksMD(InputWorkspace=mde,
                 PeaksWorkspace='predict',
                 PeakRadius=0.5,
                 OutputWorkspace='integrated')

IntegratePeaksMD(InputWorkspace=mde,
                 PeaksWorkspace='predict',
                 PeakRadius=0.5,
                 BackgroundOuterRadius=0.75,
                 OutputWorkspace='integrated_bkg')

peaks = mtd['integrated']
for p in range(peaks.getNumberPeaks()):
        peak = peaks.getPeak(p)
        if peak.getL() == 0:
            print("HKL = {:>12} int = {:>8}".format(str(peak.getHKL()),peak.getIntensity()))
