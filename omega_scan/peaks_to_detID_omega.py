from mantid.simpleapi import LoadNexus
import numpy as np

peaks = LoadNexus('peaks.nxs')

for p in range(peaks.getNumberPeaks()):
    peak = peaks.getPeak(p)
    g = peak.getGoniometerMatrix()
    detID = peak.getDetectorID()
    x=detID//(4*4*128)
    y=detID%(4*128)//4
    print(detID, peak.getQSampleFrame(), np.mod(np.arctan(g[0,2]/g[0,0])*180/np.pi,-180), x, y)
