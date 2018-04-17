import numpy as np
import time

ub = np.array([[  1.67134470e-01,   1.75052500e-01,   1.12450000e-04],
               [  1.37797000e-03,   3.61410000e-04,  -2.30940900e-02],
               [ -1.05633480e-01,   9.19279900e-02,  -1.23340000e-04]])

t0 = time.time()
data = np.load('IPTS_20367_data.npy')
phi = np.deg2rad(np.load('IPTS_20367_phi.npy'))

t1 = time.time()

output = np.zeros((401,401,251)) # -8 to 8 (x and z) -5 to 5 y
bin_size = 0.04

s2 = 2.0
detz = 0.0
k = 2*np.pi/1.488

theta = np.deg2rad(np.linspace(0,120,8*480)+s2)[::-1]
x = np.sin(theta)*72
z = np.cos(theta)*72
y = np.linspace(-10,10,512)+detz

x_array = np.tile(x,(512,1))
z_array = np.tile(z,(512,1))
y_array = np.tile(y,(8*480,1)).T
xyz=np.dstack((x_array,y_array,z_array))
xyz_norm = np.linalg.norm(xyz,axis=2)

x_array_norm = xyz[:,:,0]/xyz_norm
y_array_norm = xyz[:,:,1]/xyz_norm
z_array_norm = xyz[:,:,2]/xyz_norm-1 # Kf - Ki

qx_lab = x_array_norm*k/bin_size
qy_lab = y_array_norm*k/bin_size
qz_lab = z_array_norm*k/bin_size

t2 = time.time()

d0= -200
d1= -200
d2= -125

qlab=np.vstack((qx_lab.flatten(),qy_lab.flatten(),qz_lab.flatten())).T


for n, p in enumerate(phi):
    R = np.array([[ np.cos(p), 0, np.sin(p)],
                  [         0, 1,         0],
                  [-np.sin(p), 0, np.cos(p)]])
    RUBW = np.dot(R,ub)
    q_sample = np.dot(np.linalg.inv(RUBW),qlab.T).T
    qx_sample = np.round(q_sample[:,0]).astype(np.int)-d0
    qy_sample = np.round(q_sample[:,1]).astype(np.int)-d1
    qz_sample = np.round(q_sample[:,2]).astype(np.int)-d2                     
    np.add.at(output, (qx_sample.ravel(),
                       qy_sample.ravel(),
                       qz_sample.ravel()), data[n].ravel())

t3 = time.time()

print(t3-t2)
print(t2-t1)
print(t1-t0)

import matplotlib.pyplot as plt
plt.imshow(output[:,20,:])
plt.show()

plt.imshow(output.sum(axis=1))
plt.show()
