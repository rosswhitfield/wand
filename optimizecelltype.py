# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

#LoadWANDSCD(IPTS='7776', RunNumbers='26640-27944', Grouping='4x4', OutputWorkspace='data')
LoadMD('HB2C_WANDSCD_data.nxs', OutputWorkspace='data')
SetGoniometer('data', Axis0='s1,0,1,0,1', Average=False)
Q = ConvertHFIRSCDtoMDE(InputWorkspace='data', Wavelength=1.488)
peaks = FindPeaksMD(InputWorkspace=Q, PeakDistanceThreshold=2.2, CalculateGoniometerForCW=True, Wavelength=1.488)
FindUBUsingLatticeParameters(peaks,a=5.6,b=5.6,c=5.6,alpha=90,beta=90,gamma=90)
IndexPeaks(peaks)
TransformHKL(peaks, HKLTransform='0,1,0,0,0,1,1,0,0')
print("Starting", peaks.sample().getOrientedLattice())

OptimizeLatticeForCellType(peaks,CellType='Orthorhombic')
print("Orthorhombic", peaks.sample().getOrientedLattice())
OptimizeLatticeForCellType(peaks,CellType='Tetragonal')
print("Tetragonal", peaks.sample().getOrientedLattice())
OptimizeLatticeForCellType(peaks,CellType='Cubic')
print("Cubic", peaks.sample().getOrientedLattice())
