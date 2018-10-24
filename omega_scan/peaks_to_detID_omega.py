from mantid.simpleapi import LoadNexus

peaks = LoadNexus('peaks.nxs')

for p in range(peaks.getNumberPeaks()):
    peak = peaks.getPeak(p)
    
