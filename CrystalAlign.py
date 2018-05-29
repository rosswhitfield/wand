import numpy as np
import re

ws=LoadEventNexus(Filename='/HFIR/HB2C/IPTS-20148/nexus/HB2C_55568.nxs.h5', MetaDataOnly=True)

sgl = np.deg2rad(ws.run().getProperty('HB2C:Mot:sgl.RBV').value[0])
sgu = np.deg2rad(ws.run().getProperty('HB2C:Mot:sgu.RBV').value[0])

sgl_a = np.array([[ 1,            0,            0],
                  [ 0,  np.cos(sgl), np.sin(sgl)],
                  [ 0, -np.sin(sgl), np.cos(sgl)]])

sgu_a = np.array([[  np.cos(sgu), np.sin(sgu), 0],
                  [ -np.sin(sgu), np.cos(sgu), 0],
                  [            0,           0, 1]])


SetGoniometer(ws,
              Axis0='HB2C:Mot:sgl.RBV,1,0,0,-1')
print(ws.run().getGoniometer().getR())
print(sgl_a)

SetGoniometer(ws,
              Axis0='HB2C:Mot:sgu.RBV,0,0,1,-1')
print(ws.run().getGoniometer().getR())
print(sgu_a)


SetGoniometer(ws,
              Axis0='HB2C:Mot:sgl.RBV,1,0,0,-1',
              Axis1='HB2C:Mot:sgu.RBV,0,0,1,-1')
print(ws.run().getGoniometer().getR())
print(np.dot(sgl_a,sgu_a))




SetGoniometer(ws,
              Axis0='HB2C:Mot:s1,0,1,0,1',
              Axis1='HB2C:Mot:sgl.RBV,1,0,0,-1',
              Axis2='HB2C:Mot:sgu.RBV,0,0,1,-1')
print(ws.run().getGoniometer().getR())


UB = np.array(re.findall(r'\d+\.*\d*', ws.run().getProperty('HB2C:CS:CrystalAlign:UBMatrix').value[0]),dtype=np.float).reshape(3,3)
SetUB(ws,UB=UB)


UB_tilt = np.linalg.multi_dot((sgl_a,sgu_a,UB))


# Full test

norm=LoadWANDSCD(IPTS=7776, RunNumbers=26509, Grouping='4x4')
data=LoadWANDSCD(IPTS=20148, RunNumbers='53761-55561', Grouping='4x4')
ub=LoadWANDSCD(IPTS=20148, RunNumbers='55568', Grouping='4x4')

UB = np.array(re.findall(r'-?\d+\.*\d*', ub.getExperimentInfo(0).run().getProperty('HB2C:CS:CrystalAlign:UBMatrix').value[0]),dtype=np.float).reshape(3,3)

sgl = np.deg2rad(data.getExperimentInfo(0).run().getProperty('HB2C:Mot:sgl.RBV').value[0])
sgu = np.deg2rad(data.getExperimentInfo(0).run().getProperty('HB2C:Mot:sgu.RBV').value[0])
sgl_a = np.array([[ 1,            0,            0],
                  [ 0,  np.cos(sgl), np.sin(sgl)],
                  [ 0, -np.sin(sgl), np.cos(sgl)]])

sgu_a = np.array([[  np.cos(sgu), np.sin(sgu), 0],
                  [ -np.sin(sgu), np.cos(sgu), 0],
                  [            0,           0, 1]])

UB_new = np.linalg.multi_dot((sgl_a,sgu_a,UB))

SetUB(data,UB=UB_new)

hkl=ConvertWANDSCDtoQ('data','norm',Frame='HKL',BinningDim0='-10,10,501',BinningDim2='-10,10,501',BinningDim1='-10,10,501')


data_200=LoadWANDSCD(IPTS=20148, RunNumbers='55570-57371', Grouping='4x4')
hkl=ConvertWANDSCDtoQ('data_200','norm',Frame='HKL',BinningDim0='-5.01,5.01,501',BinningDim1='-5.01,5.01,501',BinningDim2='-2.51,0.51,151')
hkl1=ConvertWANDSCDtoQ('data_200','norm',Frame='HKL',BinningDim0='-5.01,5.01,501',BinningDim1='-5.01,5.01,501',BinningDim2='-2.51,0.51,1')
