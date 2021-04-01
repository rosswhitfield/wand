from mantid.simpleapi import *

data=LoadMD('HB2C_WANDSCD_data.nxs')
SetGoniometer(data, Axis0='s1,0,1,0,1', Average=False)
Q = ConvertHFIRSCDtoMDE(data, Wavelength=1.488)
peaks=FindPeaksMD(Q, MaxPeaks=20, PeakDistanceThreshold=0.5, DensityThresholdFactor=10000)
