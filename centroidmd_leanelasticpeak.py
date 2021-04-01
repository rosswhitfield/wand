from mantid.simpleapi import *

peaks = CreatePeaksWorkspace(NumberOfPeaks=0)
p = peaks.createPeakQSample((1,1,1)) # starting at [1,1,1]
p.setWavelength(1.54)
peaks.addPeak(p)

ws = CreateMDWorkspace(Dimensions='3', Extents='0.5,1.5,0.5,1.5,0.5,1.5',
                       Names='x,y,z', Units='rlu,rlu,rlu',
                       Frames='QSample,QSample,QSample')

# Create a fake peak at [1.1, 0.9, 1.05]
FakeMDEventData(ws, PeakParams='1000000,1.1,0.9,1.05,0.2')

centroid_peaks = CentroidPeaksMD(ws, peaks)
print("Qsample (should be approx [1.1, 0.9, 1.05]) =",centroid_peaks.getPeak(0).getQSampleFrame())
print("Wavelength =",centroid_peaks.getPeak(0).getWavelength())
