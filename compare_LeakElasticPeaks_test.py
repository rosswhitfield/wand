from mantid.simpleapi import *
from mantid.geometry import OrientedLattice
from itertools import permutations
import numpy as np

ol=OrientedLattice(5,7,12,90,90,120)
ub=ol.getUB()
print(ub)

peaks = CreatePeaksWorkspace(NumberOfPeaks=0)

peaks.addPeak(peaks.createPeakQSample(2*np.pi*np.dot(ub,[1,1,1])))
peaks.addPeak(peaks.createPeakQSample(2*np.pi*np.dot(ub,[1,1,0])))
peaks.addPeak(peaks.createPeakQSample(2*np.pi*np.dot(ub,[1,2,0])))


peaks2 = CreatePeaksWorkspace(NumberOfPeaks=0)

peaks2.addPeak(peaks2.createPeakQSample(2*np.pi*np.dot(ub,[1,1,1])))
peaks2.addPeak(peaks2.createPeakQSample(2*np.pi*np.dot(ub,[1,1,0])))
peaks2.addPeak(peaks2.createPeakQSample(2*np.pi*np.dot(ub,[1,2,0])))


CompareWorkspaces(peaks, peaks2, Tolerance=1e-4)


ws = CreateSampleWorkspace()
peaks = CreatePeaksWorkspace(InstrumentWorkspace='ws')
peaks2 = CreatePeaksWorkspace(InstrumentWorkspace='ws')
peaks.getPeak(0).setRunNumber(123)
CompareWorkspaces(peaks, peaks2, Tolerance=1e-4)
