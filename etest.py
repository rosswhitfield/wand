# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

Load(Filename='SXD23767.raw', OutputWorkspace='SXD23767', LoaderName='LoadRaw', LoaderVersion='3')
ConvertToDiffractionMDWorkspace(InputWorkspace='SXD23767', OutputWorkspace='SXD23767MD', OneEventPerBin='0')
FindSXPeaks(InputWorkspace='SXD23767', PeakFindingStrategy='AllPeaks', AbsoluteBackground=2000, 
ResolutionStrategy='AbsoluteResolution', XResolution=200, PhiResolution=3, TwoThetaResolution=3, 
OutputWorkspace='peaks')

IntegratePeaksMD(InputWorkspace='SXD23767MD', PeakRadius=0.1, Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_int', 
UseOnePercentBackgroundCorrection=False)

IntegratePeaksMD(InputWorkspace='SXD23767MD', PeakRadius='0.1,0.2,0.3', Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_int2', 
UseOnePercentBackgroundCorrection=False)

IntegratePeaksMD(InputWorkspace='SXD23767MD', PeakRadius=0.1, PeaksWorkspace='peaks', OutputWorkspace='peaks_ints', 
UseOnePercentBackgroundCorrection=False)


IntegratePeaksMD(InputWorkspace='SXD23767MD', PeakRadius='0.2,0.1,0.1', Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_intbg', 
UseOnePercentBackgroundCorrection=False, BackgroundInnerRadius='0.2,0.2,0.1', BackgroundOuterRadius='0.2,0.3,0.2')

IntegratePeaksMD(InputWorkspace='SXD23767MD', PeakRadius='0.1,0.2,0.3', Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_intbg2', 
UseOnePercentBackgroundCorrection=False, BackgroundInnerRadius='0.1,0.2,0.3', BackgroundOuterRadius='0.2,0.3,0.4')



IntegratePeaksMD(InputWorkspace='SXD23767MD', PeakRadius=0.1, Ellipsoid=False, PeaksWorkspace='peaks', OutputWorkspace='peaks_int01', 
UseOnePercentBackgroundCorrection=False)

IntegratePeaksMD(InputWorkspace='SXD23767MD', PeakRadius='0.1,0.1,0.1', Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_int02', 
UseOnePercentBackgroundCorrection=False)


IntegratePeaksMD(InputWorkspace='SXD23767MD', PeakRadius=0.1, Ellipsoid=False, PeaksWorkspace='peaks', OutputWorkspace='peaks_int11', 
UseOnePercentBackgroundCorrection=False, BackgroundInnerRadius=0.15, BackgroundOuterRadius=0.2)

IntegratePeaksMD(InputWorkspace='SXD23767MD', PeakRadius='0.1,0.1,0.1', Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_int12', 
UseOnePercentBackgroundCorrection=False, BackgroundInnerRadius='0.15,0.15,0.15', BackgroundOuterRadius='0.2,0.2,0.2')

IntegratePeaksMD(InputWorkspace='SXD23767MD', PeakRadius='0.1,0.1,0.1', Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_int03', 
UseOnePercentBackgroundCorrection=False, BackgroundInnerRadius='0.15,0.15,0.15', BackgroundOuterRadius='0.15,0.15,0.15')

IntegratePeaksMD(InputWorkspace='SXD23767MD', PeakRadius='0.1,0.1,0.1', Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_int04', 
UseOnePercentBackgroundCorrection=False, BackgroundOuterRadius='0.1,0.1,0.1')

IntegratePeaksMD(InputWorkspace='SXD23767MD', PeakRadius=0.1, Ellipsoid=False, PeaksWorkspace='peaks', OutputWorkspace='peaks_int05', 
UseOnePercentBackgroundCorrection=False, BackgroundInnerRadius=0.15, BackgroundOuterRadius=0.15)

IntegratePeaksMD(InputWorkspace='SXD23767MD', PeakRadius='0.1,0.1,0.1', Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_int06', 
UseOnePercentBackgroundCorrection=False, BackgroundOuterRadius='0.05,0.05,0.05')


IntegratePeaksMD(InputWorkspace='SXD23767MD', PeakRadius='0.1,0.1,0.1', Ellipsoid=True, PeaksWorkspace='peaks', OutputWorkspace='peaks_int21', 
UseOnePercentBackgroundCorrection=False, BackgroundOuterRadius='0.2,0.05,0.2')
