from wand import convertToQSample, convertQSampleToHKL, accumulateMD
from mantid.simpleapi import LoadNexus, LoadMD, DeleteWorkspace, DivideMD
import numpy as np

van = LoadNexus('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}.nxs'.format(6558))

if 'data' in mtd:
    DeleteWorkspace('data')

for filename in ['/HFIR/HB2C/IPTS-7776/shared/rwp/PNOe/HB2C_{}_MDE.nxs'.format(run) for run in range(4756,6557,4)]:
                 LoadMD(Filename=filename, LoadHistory=False, OutputWorkspace='md')
                 accumulateMD('md', OutputWorkspace='data')

SaveMD('data', '/HFIR/HB2C/IPTS-7776/shared/rwp/PNO_data_MDE_4.nxs')

FindPeaksMD(InputWorkspace='data', PeakDistanceThreshold=0.2, DensityThresholdFactor=1000, CalculateGoniometerForCW=True, Wavelength=1.488, OutputWorkspace='peaks')

FindUBUsingLatticeParameters('peaks',5.49,5.49,12.17,90,90,90)
ub=mtd['peaks'].sample().getOrientedLattice().getUB().copy()
print(ub)

SaveIsawUB('peaks','/HFIR/HB2C/IPTS-7776/shared/rwp/PNO_data_MDE_4.mat')

#ub=np.array([[ 0.01102186,0.18410204,0.00357398], [ 0.00136234,-0.00071337,0.07663238], [ 0.18420761,-0.01252616,-0.00416132]])

convertQSampleToHKL('data','hkl',UB=ub,Extents=[-10.025,10.025,-10.025,10.025,-2.025,2.025],Bins=[401,401,81])


if 'hkl' in mtd:
    DeleteWorkspace('hkl')
    DeleteWorkspace('hkl_norm')

for filename in ['/HFIR/HB2C/IPTS-7776/shared/rwp/PNOe/HB2C_{}_MDE.nxs'.format(run) for run in range(4756,6557,1)]:
    LoadMD(Filename=filename, LoadHistory=False, OutputWorkspace='md')
    convertQSampleToHKL('md', norm=van,UB=ub,Extents=[-10.025,10.025,-10.025,10.025,-2.025,2.025],Bins=[401,401,81],OutputWorkspace='hkl',Append=True)

norm_data=DivideMD('hkl','hkl_norm')
