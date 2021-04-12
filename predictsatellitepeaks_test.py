# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

inst = LoadEmptyInstrument(InstrumentName='TOPAZ')

peaks = CreatePeaksWorkspace(inst, NumberOfPeaks=0)

SetUB(peaks, a=2, b=2, c=2)

peak1 = peaks.createPeakHKL([1, 1, 0])
peak1.setRunNumber(1)
peaks.addPeak(peak1)
SetGoniometer(peaks, Axis0='180,0,1,0,1')
peak2 = peaks.createPeakHKL([-1, -1, 0])
peak2.setRunNumber(2)
peaks.addPeak(peak2)

satellite = PredictSatellitePeaks(peaks, ModVector1='0.2,0,0', MaxOrder=1)

peaks = CreatePeaksWorkspace(NumberOfPeaks=0, OutputType='LeanElasticPeak')

SetUB(peaks, a=2, b=2, c=2)

peak1 = peaks.createPeakHKL([1, 1, 0])
peak1.setRunNumber(1)
peaks.addPeak(peak1)
SetGoniometer(peaks, Axis0='180,0,1,0,1')
peak2 = peaks.createPeakHKL([-1, -1, 0])
peak2.setRunNumber(2)
peaks.addPeak(peak2)

satellite2 = PredictSatellitePeaks(peaks, ModVector1='0.2,0,0', MaxOrder=1)

#peaks3 = PredictPeaks(peaks, MinDSpacing=1.95, MaxDSpacing=2.05,OutputType='LeanElasticPeak', CalculateWavelength=False)
satellite3 = PredictSatellitePeaks(peaks, ModVector1='0.2,0,0', MaxOrder=1, IncludeAllPeaksInRange=True, MinDSpacing=1.9, MaxDSpacing=2.1)
