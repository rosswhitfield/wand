# The following line helps with future compatibility with Python 3
# print must now be used as a function, e.g print('Hello','World')
from __future__ import (absolute_import, division, print_function, unicode_literals)

# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *

import matplotlib.pyplot as plt

import numpy as np

data = LoadWANDSCD(IPTS=22745, RunNumbers='147131-148931', Grouping='4x4')
mde=ConvertWANDSCDtoMDE(data, wavelenght=1.488)

PredictPeaks(InputWorkspace='Q',
             MinDSpacing=0.1,
             CalculateGoniometerForCW=True,
             Wavelength=1.488, MaxAngle=0,
             CalculateStructureFactors=True,
             OutputWorkspace='predict')

FindPeaksMD(InputWorkspace='mde',
            PeakDistanceThreshold=1,
            DensityThresholdFactor=10000,
            CalculateGoniometerForCW=True,
            OutputWorkspace='peaks')
