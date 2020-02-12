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


# Add structure to workspace to allow calcualting the Sturcture Factors in PredictPeaks
cs = CrystalStructure('4.75903 4.75902 12.9826',
'R -3 c',
"""Al 0 0 0.35218 1.0 0.00327; O 0.30625 0 0.25 1.0 0.00387""")
data.getExperimentInfo(0).sample().setCrystalStructure(cs)
unitCell = cs.getUnitCell()
print('Unit cell: {0} {1} {2} {3} {4} {5}'.format(unitCell.a(), unitCell.b(), unitCell.c(), unitCell.alpha(), unitCell.beta(), unitCell.gamma()))
scatterers = cs.getScatterers()
print('Total number of scatterers: {0}'.format(len(scatterers)))
for i, scatterer in enumerate(scatterers):
    print('  {0}: {1}'.format(i,scatterer))


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


IntegratePeaksMD(InputWorkspace=mde2,
                 PeaksWorkspace='predict',
                 PeakRadius=0.5,
                 OutputWorkspace='integrated2')

IntegratePeaksMD(InputWorkspace=mde2,
                 PeaksWorkspace='predict',
                 PeakRadius=0.5,
                 BackgroundOuterRadius=0.75,
                 OutputWorkspace='integrated2_bkg')
