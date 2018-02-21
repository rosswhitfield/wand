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
SaveIsawUB('peaks','/HFIR/HB2C/IPTS-7776/shared/rwp/PNO_data_MDE_4.mat')

#CreateSingleValuedWorkspace(OutputWorkspace='ub')
#LoadIsawUB('ub','/HFIR/HB2C/IPTS-7776/shared/rwp/PNO_data_MDE_4.mat')
#ub=mtd['ub'].sample().getOrientedLattice().getUB().copy()


ub=mtd['peaks'].sample().getOrientedLattice().getUB().copy()
print(ub)

#ub=np.array([[ 0.01102186,0.18410204,0.00357398], [ 0.00136234,-0.00071337,0.07663238], [ 0.18420761,-0.01252616,-0.00416132]])

convertQSampleToHKL('data','data_hkl',UB=ub,Extents=[-10.025,10.025,-10.025,10.025,-2.025,2.025],Bins=[401,401,81])


if 'hkl' in mtd:
    DeleteWorkspace('hkl')
    DeleteWorkspace('hkl_norm')

for filename in ['/HFIR/HB2C/IPTS-7776/shared/rwp/PNOe/HB2C_{}_MDE.nxs'.format(run) for run in range(4756,6557,1)]:
    LoadMD(Filename=filename, LoadHistory=False, OutputWorkspace='md')
    convertQSampleToHKL('md', norm=van,UB=ub,Extents=[-7.01,7.01,-7.01,7.01,-2.01,2.01],Bins=[701,701,201],OutputWorkspace='hkl',Append=True)

SaveMD('hkl', '/HFIR/HB2C/IPTS-7776/shared/rwp/PNO_data_MDH_0.2.nxs')
SaveMD('hkl_norm', '/HFIR/HB2C/IPTS-7776/shared/rwp/PNO_norm_MDH_0.2.nxs')


norm_data=DivideMD('hkl','hkl_norm')



# Symmerty

CloneMDWorkspace('hkl',OutputWorkspace='hkl_sym')
CloneMDWorkspace('hkl_norm',OutputWorkspace='hkl_norm_sym')

data_signal = mtd['hkl'].getSignalArray()
norm_signal = mtd['hkl_norm'].getSignalArray()

data_signal_new = data_signal + data_signal[::-1,::-1,::1] # 180
norm_signal_new = norm_signal + norm_signal[::-1,::-1,::1] # 180

data_signal_new = data_signal + np.transpose(data_signal,(1,0,2))[::-1,::1,::1] + data_signal[::-1,::-1,::1]  + np.transpose(data_signal,(1,0,2))[::1,::-1,::1] # 90. 180. 270
norm_signal_new = norm_signal + np.transpose(norm_signal,(1,0,2))[::-1,::1,::1] + norm_signal[::-1,::-1,::1]  + np.transpose(norm_signal,(1,0,2))[::1,::-1,::1] # 90, 180, 270

data_signal_new = data_signal_new + data_signal_new[::-1,::1,::1] # mirror x
norm_signal_new = norm_signal_new+ norm_signal_new[::-1,::1,::1] # mirror x
data_signal_new = data_signal_new + data_signal_new[::1,::-1,::1] # mirror y
norm_signal_new = norm_signal_new+ norm_signal_new[::1,::-1,::1] # mirror y


mtd['hkl_sym'].setSignalArray(data_signal_new)
mtd['hkl_norm_sym'].setSignalArray(norm_signal_new)

norm_data_sym=DivideMD('hkl_sym','hkl_norm_sym')
