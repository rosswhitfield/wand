from mantid.simpleapi import LoadNexus
import numpy as np

peaks = LoadNexus('peaks.nxs')

for p in range(peaks.getNumberPeaks()):
    peak = peaks.getPeak(p)
    g = peak.getGoniometerMatrix()
    print(peak.getDetectorID(), peak.getQSampleFrame(), np.mod(np.arctan(g[0,2]/g[0,0])*180/np.pi,-180))
