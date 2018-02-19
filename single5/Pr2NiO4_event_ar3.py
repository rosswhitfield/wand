from mantid.simpleapi import *

if 'dataE' in mtd:
    mtd.remove('dataE')
    
for run in range(4756,6557,5):
    LoadMD(Filename='/HFIR/HB2C/IPTS-7776/shared/rwp/PNOe/HB2C_{}_MDE.nxs'.format(run),OutputWorkspace='md')
    if 'dataE' in mtd:
        PlusMD(LHSWorkspace='dataE', RHSWorkspace='md', OutputWorkspace='dataE')
    else:
        CloneMDWorkspace(InputWorkspace='md', OutputWorkspace='dataE')

FindPeaksMD(InputWorkspace='dataE', PeakDistanceThreshold=0.2, DensityThresholdFactor=2000, CalculateGoniometerForCW=True, Wavelength=1.488, OutputWorkspace='peaks')
FindUBUsingFFT('peaks',MinD=3,MaxD=15)
ShowPossibleCells('peaks')
SelectCellWithForm('peaks',FormNumber=13,Apply=True)
OptimizeLatticeForCellType('peaks', CellType='Orthorhombic',Apply=True)
ub=mtd['peaks'].sample().getOrientedLattice().getUB().copy()

FindUBUsingLatticeParameters('peaks',5.49,5.49,12.17,90,90,90)
ub=mtd['peaks'].sample().getOrientedLattice().getUB().copy()


ol = OrientedLattice()
ol.setUB(ub)
q1 = ol.qFromHKL([1, 0, 0])
q2 = ol.qFromHKL([0, 1, 0])
q3 = ol.qFromHKL([0, 0, 1])

BinMD(InputWorkspace='dataE',OutputWorkspace='mdh', AxisAligned=False, NormalizeBasisVectors=False,
          BasisVector0='[H,0,0],A^-1,{},{},{}'.format(q1.X(), q1.Y(), q1.Z()),
          BasisVector1='[0,K,0],A^-1,{},{},{}'.format(q2.X(), q2.Y(), q2.Z()),
          BasisVector2='[0,0,L],A^-1,{},{},{}'.format(q3.X(), q3.Y(), q3.Z()),
          OutputExtents='-8,8,-8,8,-2.5,2.5', OutputBins='401,401,126')
