# The following line helps with future compatibility with Python 3
# print must now be used as a function, e.g print('Hello','World')
from __future__ import (absolute_import, division, print_function, unicode_literals)

# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *

import matplotlib.pyplot as plt

import numpy as np

data = LoadWANDSCD(IPTS=22745, RunNumbers='145330-147130')
mde = ConvertHFIRSCDtoMDE(data, wavelength=1.488,MinValues='-10,-10,-10',MaxValues='10,10,10')

data2 = LoadWANDSCD(IPTS=22745, RunNumbers='147131-148931')
mde2 = ConvertHFIRSCDtoMDE(data2, wavelength=1.488,MinValues='-10,-10,-10',MaxValues='10,10,10')


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


IntegratePeaksMD(InputWorkspace=mde,
                 PeaksWorkspace='predict',
                 PeakRadius=0.5,
                 OutputWorkspace='integrated2')

IntegratePeaksMD(InputWorkspace=mde,
                 PeaksWorkspace='predict',
                 PeakRadius=0.5,
                 BackgroundOuterRadius=0.75,
                 OutputWorkspace='integrated2_bkg')
