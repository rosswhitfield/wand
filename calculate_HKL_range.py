workspace_name = 'data'

Uproj = [1, 0, 0]
Vproj = [0, 1, 0]
Wproj = [0, 0, 1]

wavelength = 1.488

################################################################################

import numpy as np

ws=mtd[workspace_name]
s1 = np.deg2rad(ws.getExperimentInfo(0).run().getProperty('s1').value)
polar = np.array(ws.getExperimentInfo(0).run().getProperty('twotheta').value)
polar = np.hstack((polar[::64], polar[63::64]))
azim = np.array(ws.getExperimentInfo(0).run().getProperty('azimuthal').value)
azim = np.hstack((azim[::64], azim[63::64]))
UB = ws.getExperimentInfo(0).sample().getOrientedLattice().getUB()

k = 1/wavelength

qlab = np.vstack((np.sin(polar)*np.cos(azim),
                  np.sin(polar)*np.sin(azim),
                  np.cos(polar) - 1)).T * -k

W = np.eye(3)
W[:,0] = Uproj
W[:,1] = Vproj
W[:,2] = Wproj

UBW = np.dot(UB, W)

HKL_min = np.array([1e9,1e9,1e9])
HKL_max = np.array([-1e9,-1e9,-1e9])

for rot in s1:
    R = np.array([[ np.cos(rot), 0, np.sin(rot)],
                  [           0, 1,           0],
                  [-np.sin(rot), 0, np.cos(rot)]])
    RUBW = np.dot(R,UBW)
    HKL=np.dot(np.linalg.inv(RUBW),qlab.T)
    HKL_min = np.minimum(HKL_min, HKL.min(axis=1))
    HKL_max = np.maximum(HKL_max, HKL.max(axis=1))

fmt = '{:>12} min: {: .4f} max: {: .4f}'
print(fmt.format(str(Uproj), HKL_min[0], HKL_max[0]))
print(fmt.format(str(Vproj), HKL_min[1], HKL_max[1]))
print(fmt.format(str(Wproj), HKL_min[2], HKL_max[2]))
