# The following line helps with future compatibility with Python 3
# print must now be used as a function, e.g print('Hello','World')
from __future__ import (absolute_import, division, print_function, unicode_literals)

# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *

import matplotlib.pyplot as plt

import numpy as np

data = LoadWANDSCD(IPTS=21362, RunNumbers='120754-122554', Grouping='4x4')
norm=LoadWANDSCD("HB2C137518", Grouping='4x4')
mde=ConvertWANDSCDtoMDE(data)
ConvertWANDSCDtoQ(InputWorkspace='data',
                  NormalisationWorkspace='norm',
                  OutputWorkspace='Q',
                  BinningDim1='-1,1,21')
PredictPeaks(InputWorkspace='Q',
MinDSpacing=0.1,
CalculateGoniometerForCW=True,
Wavelength=1.488, MaxAngle=0,
CalculateStructureFactors=True,
OutputWorkspace='predict')
