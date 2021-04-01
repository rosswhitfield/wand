from mantid.simpleapi import *
import numpy as np
import math
from mantid.geometry import Goniometer
from mantid.kernel import V3D


HB3AAdjustSampleNorm(Filename="HB3A_exp0724_scan0183.nxs", OutputWorkspace='data')



peaks = PredictPeaks("data",
                     ReflectionCondition='B-face centred',
                     CalculateGoniometerForCW=True,
                     Wavelength=1.008,
                     InnerGoniometer=True,
                     FlipX=True,
                     MinAngle=-2,
                     MaxAngle=90)

leanelasticpeaks = PredictPeaks("data",
                                ReflectionCondition='B-face centred',
                                CalculateGoniometerForCW=True,
                                Wavelength=1.008,
                                InnerGoniometer=True,
                                FlipX=True,
                                MinAngle=-2,
                                MaxAngle=90,
                                OutputType='LeanElasticPeak')
int_peaks = IntegratePeaksMD("data", "leanelasticpeaks", PeakRadius=0.1)

leanelasticpeaks2 = PredictPeaks("data",
                                ReflectionCondition='B-face centred',
                                OutputType='LeanElasticPeak', CalculateWavelength=False)
int_peaks2 = IntegratePeaksMD("data", "leanelasticpeaks2", PeakRadius=0.1)
filter_int_peaks2 = FilterPeaks(int_peaks2, FilterVariable='Intensity', FilterValue=0, Operator='>')

HFIRCalculateGoniometer(filter_int_peaks2)

leanelasticpeaks3 = PredictPeaks("data",
                                ReflectionCondition='B-face centred',
                                OutputType='LeanElasticPeak')

ws=CreatePeaksWorkspace()
SetUB(ws,a=2,b=2,c=2)
p = PredictPeaks(ws, OutputType='LeanElasticPeak', CalculateWavelength=False)


peaks = leanelasticpeaks3

wavelength = peaks.run()['wavelength'].value

flip_x = peaks.getInstrument().getName() == "HB3A"

if peaks.getInstrument().getName() == "HB3A":
    inner = math.isclose(peaks.run().getTimeAveragedStd("omega"), 0.0)
else:
    inner = False

for n in range(peaks.getNumberPeaks()):
    p = peaks.getPeak(n)
    g = Goniometer()
    g.calcFromQSampleAndWavelength(V3D(*p.getQSampleFrame()), wavelength, flip_x, inner)
    p.setWavelength(wavelength)
    p.setGoniometerMatrix(g.getR())
    print(g.getEulerAngles('YZY'))
