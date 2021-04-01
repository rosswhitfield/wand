from mantid.simpleapi import *
import numpy as np
from scipy.stats import multivariate_normal

## FindPeaksMD test MDEvent
mde = CreateMDWorkspace(Dimensions='3', Extents='0,10,0,10,0,10',
                       Names='Q_sample_x,Q_sample_y,Q_sample_z',
                       Units='rlu,rlu,rlu',
                       Frames='QSample,QSample,QSample')
FakeMDEventData(mde, PeakParams='10000,1,1,1,0.2')
FakeMDEventData(mde, PeakParams='100000,3,3,3,0.3')
FakeMDEventData(mde, PeakParams='1000,5.5,3.14159,1,0.1')

peaks=FindPeaksMD(mde,
                  DensityThresholdFactor=1,
                  PeakDistanceThreshold=0.5)

for n in range(peaks.getNumberPeaks()):
    print(peaks.getPeak(n).getQSampleFrame())

## FindPeaksMD test MDHisto

x, y, z = np.mgrid[0:10:300j, 0:10:300j, 0:10:300j]
# Need an (N, 2) array of (x, y) pairs.
xyz = np.column_stack([x.flat, y.flat, z.flat])

p1 = multivariate_normal.pdf(xyz,
                             mean=[1.0, 1.0, 1.0],
                             cov=np.diag([0.04, 0.04, 0.04])) * 1000
p2 = multivariate_normal.pdf(xyz,
                             mean=[3.0, 3.0, 3.0],
                             cov=np.diag([0.09, 0.09, 0.09])) * 10000
p3 = multivariate_normal.pdf(xyz,
                             mean=[5.5, 3.14159, 1.0],
                             cov=np.diag([0.0025, 0.0025, 0.0025])) * 100

s = p1 + p2 + p3

mdh = CreateMDHistoWorkspace(SignalInput=s,
                             ErrorInput=s,
                             Dimensionality=3,
                             Extents='0,10,0,10,0,10',
                             NumberOfBins='300,300,300',
                             Names='Q_sample_x,Q_sample_y,Q_sample_z',
                             Units='rlu,rlu,rlu',
                             Frames='QSample,QSample,QSample')

peaks=FindPeaksMD(mdh,
                  DensityThresholdFactor=600,
                  PeakDistanceThreshold=0.5)

for n in range(peaks.getNumberPeaks()):
    print(peaks.getPeak(n).getQSampleFrame())


# TOPAZ test
LoadEventNexus(Filename='./ExternalData/Testing/Data/SystemTest/TOPAZ_3132_event.nxs',OutputWorkspace='topaz_3132')
ConvertToDiffractionMDWorkspace(InputWorkspace='topaz_3132',OutputWorkspace='topaz_3132_MD', OutputDimensions='Q (sample frame)',
                                LorentzCorrection='1',SplitInto='2',SplitThreshold='150',OneEventPerBin='0')
FindPeaksMD(InputWorkspace='topaz_3132_MD',PeakDistanceThreshold='0.12',MaxPeaks='200',OutputWorkspace='peaks')
FindPeaksMD(InputWorkspace='topaz_3132_MD',PeakDistanceThreshold='0.12',MaxPeaks='200',OutputType='LeanElasticPeak',OutputWorkspace='leanpeaks')


# WAND test
LoadMD('./ExternalData/Testing/Data/SystemTest/HB2C_WANDSCD_data.nxs', OutputWorkspace='ConvertHFIRSCDtoMDETest_data')
SetGoniometer('ConvertHFIRSCDtoMDETest_data', Axis0='s1,0,1,0,1', Average=False)
ConvertHFIRSCDtoMDETest_Q = ConvertHFIRSCDtoMDE(InputWorkspace='ConvertHFIRSCDtoMDETest_data', Wavelength=1.488)
ConvertHFIRSCDtoMDETest_peaks = FindPeaksMD(InputWorkspace=ConvertHFIRSCDtoMDETest_Q, PeakDistanceThreshold=2.2,
                                                    CalculateGoniometerForCW=True, Wavelength=1.488)
ConvertHFIRSCDtoMDETest_leanpeaks = FindPeaksMD(InputWorkspace=ConvertHFIRSCDtoMDETest_Q, PeakDistanceThreshold=2.2,
                                                    OutputType='LeanElasticPeak')


LoadMD('./ExternalData/Testing/Data/SystemTest/HB2C_WANDSCD_norm.nxs', OutputWorkspace='ConvertWANDSCDtoQTest_norm')
ConvertWANDSCDtoQTest_Q = ConvertWANDSCDtoQ(InputWorkspace='ConvertHFIRSCDtoMDETest_data',
                                                    NormalisationWorkspace='ConvertWANDSCDtoQTest_norm')
ConvertWANDSCDtoQTest_peaks = FindPeaksMD(InputWorkspace=ConvertWANDSCDtoQTest_Q, PeakDistanceThreshold=2,
                                                  CalculateGoniometerForCW=True, Wavelength=1.488)

from mantid.geometry import Goniometer
wavelength = 1.488
for n in range(ConvertHFIRSCDtoMDETest_leanpeaks.getNumberPeaks()):
    p = ConvertHFIRSCDtoMDETest_leanpeaks.getPeak(n)
    g = Goniometer()
    g.calcFromQSampleAndWavelength(p.getQSampleFrame(), wavelength)
    p.setWavelength(wavelength)
    p.setGoniometerMatrix(g.getR())
    print(g.getEulerAngles('YZY'))