from mantid.simpleapi import *

LoadMD('HB3A_data.nxs', OutputWorkspace='ConvertHFIRSCDtoMDE_HB3ATest_data')

SetGoniometer('ConvertHFIRSCDtoMDE_HB3ATest_data',
              Axis0='omega,0,1,0,-1',
              Axis1='chi,0,0,1,-1',
              Axis2='phi,0,1,0,-1',
              Average=False)

ConvertHFIRSCDtoMDETest_Q = ConvertHFIRSCDtoMDE(InputWorkspace='ConvertHFIRSCDtoMDE_HB3ATest_data',
                                                Wavelength=1.008)

peaks=FindPeaksMD(ConvertHFIRSCDtoMDETest_Q, MaxPeaks=2, PeakDistanceThreshold=0.5, DensityThresholdFactor=10000)

print(peaks.column(5))

SaveMD(ConvertHFIRSCDtoMDETest_Q,'/SNS/users/rwp/test_md.nxs')

a=LoadMD('/SNS/users/rwp/test_md2.nxs')
peaks2=FindPeaksMD(a, MaxPeaks=2, PeakDistanceThreshold=0.5, DensityThresholdFactor=10000)

print(peaks2.column(5))
