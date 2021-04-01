from mantid.simpleapi import *
from mantid.geometry import OrientedLattice
from itertools import permutations
import numpy as np

ol=OrientedLattice(5,7,12,90,90,120)
ub=ol.getUB()
print(ub)

peaks = CreatePeaksWorkspace(NumberOfPeaks=0)

for hkl in set(permutations([1,1,1,0,0,0,-1,-1,-1],3)):
    p = peaks.createPeakQSample(2*np.pi*np.dot(ub,hkl))
    peaks.addPeak(p)

#sorted_peaks = SortPeaksWorkspace(peaks, ColumnNameToSortBy='DSpacing')

FindUBUsingFFT(peaks, MinD=3, MaxD=20)
ShowPossibleCells(peaks)

print(peaks.sample().getOrientedLattice().getUB())

FindUBUsingLatticeParameters(peaks, a=5,b=7,c=12,alpha=90,beta=90,gamma=120)
ShowPossibleCells(peaks)
print(peaks.sample().getOrientedLattice().getUB())

SelectCellWithForm(peaks, 34)
SelectCellOfType(peaks, CellType='Monoclinic', Centering='P')

CalculatePeaksHKL(peaks)

IndexPeaks(peaks)

TransformHKL(peaks, HKLTransform='1,0,0,0,2,0,0,0,3')

FindUBUsingIndexedPeaks(peaks)

filtered_peaks = FilterPeaks(peaks, FilterVariable='h+k+l', FilterValue=3, Operator='=')

ws = CreateMDWorkspace(Dimensions='3', Extents='0.5,1.5,0.5,1.5,0.5,1.5',
                       Names='x,y,z', Units='rlu,rlu,rlu',
                       Frames='QSample,QSample,QSample')
nevents=100000
FakeMDEventData(ws, UniformParams=nevents)

peaks2 = CreatePeaksWorkspace(NumberOfPeaks=0)
p = peaks2.createPeakQSample((1,1,1))
peaks2.addPeak(p)

radius = 0.5
int_peaks = IntegratePeaksMD(ws, peaks2, PeakRadius=radius)
print('Integrated Intensity =', int_peaks.getPeak(0).getIntensity())
print('Approx. Expected Intensity =', 4/3*np.pi*radius**3*nevents)

combined_peaks = CombinePeaksWorkspaces(peaks, int_peaks)

## CentroidPeaksMD test
ws = CreateMDWorkspace(Dimensions='3', Extents='0.5,1.5,0.5,1.5,0.5,1.5',
                       Names='x,y,z', Units='rlu,rlu,rlu',
                       Frames='QSample,QSample,QSample')
FakeMDEventData(ws, PeakParams='1000000,1.1,0.9,1.05,0.2')

centroid_peaks = CentroidPeaksMD(ws, peaks2)
print("Qsample (should be approx [1.1, 0.9, 1.05]) =",centroid_peaks.getPeak(0).getQSampleFrame())

SaveReflections(combined_peaks, Filename='/tmp/peaks.fullprof.txt', Format='Fullprof')
SaveReflections(combined_peaks, Filename='/tmp/peaks.jana.txt', Format='Jana')
#SaveReflections(combined_peaks, Filename='/tmp/peaks.gsas.txt', Format='GSAS')
#SaveReflections(combined_peaks, Filename='/tmp/peaks.shelx.txt', Format='SHELX')

SaveHKLCW(combined_peaks,'/tmp/peaks.savehklcw.txt')


SaveNexus(combined_peaks, Filename='/tmp/peaks.nxs')
loaded_peaks = LoadNexus('/tmp/peaks.nxs')
