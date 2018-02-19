from mantid.simpleapi import *

if 'dataE' in mtd:
    mtd.remove('dataE')
    
for run in range(4756,6557,5):
    LoadMD(Filename='/HFIR/HB2C/IPTS-7776/shared/rwp/PNOe/HB2C_{}_MDE.nxs'.format(run),OutputWorkspace='md')
    if 'dataE' in mtd:
        PlusMD(LHSWorkspace='dataE', RHSWorkspace='md', OutputWorkspace='dataE')
    else:
        CloneMDWorkspace(InputWorkspace='md', OutputWorkspace='dataE')

FindPeaksMD(InputWorkspace='dataE', PeakDistanceThreshold=0.2, DensityThresholdFactor=500, CalculateGoniometerForCW=True, Wavelength=1.488, OutputWorkspace='peaks')
FindUBUsingFFT('peaks',MinD=3,MaxD=15)
ShowPossibleCells('peaks')
SelectCellWithForm('peaks',FormNumber=42,Apply=True)
OptimizeLatticeForCellType('peaks', CellType='Orthorhombic',Apply=True)
#SaveIsawUB('peaks',Filename='/SNS/users/rwp/PNO.mat')
