# The following line helps with future compatibility with Python 3
# print must now be used as a function, e.g print('Hello','World')
from __future__ import (absolute_import, division, print_function, unicode_literals)

# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *

import matplotlib.pyplot as plt

import numpy as np

data = LoadWANDSCD(IPTS=21362, RunNumbers='120754-122554', Grouping='4x4')
norm=LoadWANDSCD(IPTS=7776,RunNumbers='137518', Grouping='4x4')
mde=ConvertWANDSCDtoMDE(data)
ConvertWANDSCDtoQ(InputWorkspace='data',
                  NormalisationWorkspace='norm',
                  OutputWorkspace='Q',
                  BinningDim1='-1,1,21')
ConvertWANDSCDtoQ(InputWorkspace='data',
                  NormalisationWorkspace='norm',
                  Frame='HKL',
                  OutputWorkspace='HKL',
                  BinningDim0='-5.01,5.01,501',
                  BinningDim1='-5.01,5.01,501',
                  BinningDim2='-0.21,0.81,51')

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


FindPeaksMD(InputWorkspace='mde', PeakDistanceThreshold=1, DensityThresholdFactor=10000, CalculateGoniometerForCW=True, OutputWorkspace='peaks')
IndexPeaks(PeaksWorkspace='peaks')
OptimizeLatticeForCellType(PeaksWorkspace='peaks', CellType='Hexagonal', Apply=True, OutputDirectory='/home/rwp/build/mantid/.')

PredictPeaks(InputWorkspace='peaks',
MinDSpacing=0.1,
CalculateGoniometerForCW=True,
Wavelength=1.488,
MaxAngle=0,
ReflectionCondition='Hexagonally centred, reverse',
CalculateStructureFactors=True,
OutputWorkspace='predict2')

CopySample(InputWorkspace='peaks',
OutputWorkspace='data',
CopyMaterial=False, CopyEnvironment=False, CopyShape=False
)


ConvertWANDSCDtoQ(InputWorkspace='data',
                  NormalisationWorkspace='norm',
                  Frame='HKL',
                  OutputWorkspace='HKL2',
                  BinningDim0='-5.01,5.01,501',
                  BinningDim1='-5.01,5.01,501',
                  BinningDim2='-0.21,0.81,51')



#PredictFractionalPeaks(Peaks='peaks', FracPeaks='frac', HOffset='0.5,0,0', KOffset='0,0.5,0', LOffset='0,0,0.25')



FindPeaksMD(InputWorkspace='mde', PeakDistanceThreshold=1, DensityThresholdFactor=1, CalculateGoniometerForCW=True, OutputWorkspace='peaks2')
IndexPeaks(PeaksWorkspace='peaks2',RoundHKLs=False)


PredictPeaks(InputWorkspace='peaks',
MinDSpacing=0.1,
CalculateGoniometerForCW=True,
Wavelength=1.488,
MaxAngle=0,
ReflectionCondition='Hexagonally centred, reverse',
CalculateStructureFactors=True,
OutputWorkspace='predict2')


CloneWorkspace(InputWorkspace='peaks', OutputWorkspace='peaks2')

ol=mtd['peaks2'].sample().getOrientedLattice()
a=ol.a();
b=ol.b()
c=ol.c()
ol.seta(a*4)
ol.setb(b*4)
ol.setc(c*4)

PredictPeaks(InputWorkspace='peaks2',
MinDSpacing=0.1,
CalculateGoniometerForCW=True,
Wavelength=1.488,
MaxAngle=0,
ReflectionCondition='Hexagonally centred, reverse',
CalculateStructureFactors=True,
OutputWorkspace='predict2')







#####


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
FindPeaksMD(InputWorkspace='mde',
PeakDistanceThreshold=1,
DensityThresholdFactor=10000,
CalculateGoniometerForCW=True,
OutputWorkspace='peaks')
IndexPeaks(PeaksWorkspace='peaks')
OptimizeLatticeForCellType(PeaksWorkspace='peaks', CellType='Hexagonal', Apply=True)

ConvertWANDSCDtoQ(InputWorkspace='data',
                  NormalisationWorkspace='norm',
                  UBWorkspace='peaks',
                  Frame='HKL',
                  OutputWorkspace='HKL',
                  BinningDim0='-5.01,5.01,501',
                  BinningDim1='-5.01,5.01,501',
                  BinningDim2='-0.21,0.81,51')

PredictPeaks(InputWorkspace='peaks',
MinDSpacing=0.1,
CalculateGoniometerForCW=True,
Wavelength=1.488,
MaxAngle=0,
ReflectionCondition='Hexagonally centred, reverse',
CalculateStructureFactors=True,
OutputWorkspace='predict')


FindPeaksMD(InputWorkspace='mde',
PeakDistanceThreshold=0.25,
#DensityThresholdFactor=10000,
CalculateGoniometerForCW=True,
OutputWorkspace='peaks2')
FilterPeaks(InputWorkspace='peaks2', OutputWorkspace='peaks2_filtered', FilterVariable='QMod', Operator='>', FilterValue=1.5)
IndexPeaks(PeaksWorkspace='peaks2', RoundHKLs=False)




LoadWANDSCD(IPTS=21362, RunNumbers='120754-122554', Grouping='4x4', OutputWorkspace='data')
ConvertWANDSCDtoMDE(InputWorkspace='data', OutputWorkspace='mde')
FindPeaksMD(InputWorkspace='mde', PeakDistanceThreshold=0.25, CalculateGoniometerForCW=True, OutputWorkspace='peaks2')
FilterPeaks(InputWorkspace='peaks2', OutputWorkspace='peaks2_filtered', FilterVariable='QMod', FilterValue=1.5, Operator='>')
FindUBUsingLatticeParameters(PeaksWorkspace='peaks2_filtered', a=4, b=4, c=4, alpha=90, beta=90, gamma=120)
OptimizeLatticeForCellType(PeaksWorkspace='peaks2_filtered', CellType='Hexagonal', Apply=True)
